import os
import time
import psutil
import platform
import threading
import datetime
import json
from typing import Dict, Optional, List, Any
import atexit
from pathlib import Path
import uuid
import sys
from ..utils.logger import logger


class ResourceMonitor:
    """Monitor and record system resource usage during req-test-align operations"""

    def __init__(self, source_type: str, operation_type: str):
        """
        Initialize the resource monitor

        Args:
            source_type: The type of invocation ('git_hook', 'vscode', 'github_actions', 'cli')
            operation_type: The operation being performed (e.g., 'generate', 'configure')
        """
        self.source_type = source_type
        self.operation_type = operation_type
        self.start_time = time.time()
        self.end_time = None
        self.session_id = str(uuid.uuid4())

        # Sampling intervals in seconds
        self.sampling_interval = 0.5

        self.metrics = {
            "session_id": self.session_id,
            "source_type": source_type,
            "operation_type": operation_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "process_cpu_samples": [],
            "process_memory_samples": [],
            "process_io_samples": [],
            "process_threads_samples": [],
            "duration": None,
            "peak_values": {},
            "average_values": {},
        }

        # Get process information
        self.process = psutil.Process(os.getpid())

        # Save process info
        self.metrics["process_info"] = {
            "pid": self.process.pid,
            "name": self.process.name(),
            "create_time": datetime.datetime.fromtimestamp(
                self.process.create_time()
            ).isoformat(),
            "cmdline": self.process.cmdline(),
        }

        # Additional process metrics
        self.metrics["process_cpu_samples"] = []
        self.metrics["process_memory_samples"] = []
        self.metrics["process_io_samples"] = []
        self.metrics["process_threads_samples"] = []

        # Get base network stats for calculating deltas
        self.last_disk_io = psutil.disk_io_counters()
        self.last_sample_time = time.time()

        # Monitoring thread
        self.keep_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.daemon = True

        # Register cleanup at exit
        atexit.register(self.stop_and_save)

        # Determine output directory
        self.output_dir = self._get_output_directory()

        # Start monitoring
        self.monitor_thread.start()
        logger.debug(
            f"Resource monitoring started for {source_type} - {operation_type} (Session ID: {self.session_id})"
        )

        self.metrics["cpu_info"] = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "max_frequency_mhz": getattr(psutil.cpu_freq(), "max", None),
        }

        # Try to get more detailed CPU info
        try:
            import cpuinfo

            cpu_info = cpuinfo.get_cpu_info()
            self.metrics["cpu_info"].update(
                {
                    "model": cpu_info.get("brand_raw", "Unknown"),
                    "architecture": cpu_info.get("arch", platform.machine()),
                    "bits": cpu_info.get("bits", 64),
                    "vendor": cpu_info.get("vendor_id_raw", "Unknown"),
                }
            )
        except ImportError:
            # If cpuinfo is not available, try to get CPU model from platform
            if platform.system() == "Windows":
                self.metrics["cpu_info"]["model"] = platform.processor()
            elif platform.system() == "Linux":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line:
                                self.metrics["cpu_info"]["model"] = line.split(":")[
                                    1
                                ].strip()
                                break
                except:
                    self.metrics["cpu_info"]["model"] = "Unknown"

    def _get_output_directory(self) -> Path:
        """Determine where to save metrics data"""
        # Try to use an environment variable first
        output_dir = os.environ.get("REQ_TEST_ALIGN_METRICS_DIR")

        if output_dir:
            path = Path(output_dir)
        else:
            # Default to user's home directory under .req-test-align/metrics
            path = Path.home() / ".req-test-align" / "metrics"

        # Ensure directory exists
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _monitor_resources(self):
        """Continuously monitor resource usage of the current process"""
        try:
            # Initialize process network tracking
            last_connections = set()
            last_net_io = {"bytes_sent": 0, "bytes_recv": 0}

            while self.keep_monitoring:
                # Process CPU usage (percent of a single core)
                process_cpu_percent = self.process.cpu_percent(interval=None)

                # Process memory usage
                process_memory = self.process.memory_info()

                # Current time for interval calculation
                current_time = time.time()
                time_delta = current_time - self.last_sample_time

                # Process IO counters
                try:
                    process_io = self.process.io_counters()
                except (psutil.AccessDenied, AttributeError):
                    process_io = None

                # Process threads
                process_threads = self.process.num_threads()

                # Update last sample time
                self.last_sample_time = current_time

                # Record process-specific metrics
                self.metrics["process_cpu_samples"].append(
                    {
                        "timestamp": time.time() - self.start_time,
                        "percent": process_cpu_percent,
                    }
                )

                self.metrics["process_memory_samples"].append(
                    {
                        "timestamp": time.time() - self.start_time,
                        "rss_mb": process_memory.rss / (1024 * 1024),
                        "vms_mb": process_memory.vms / (1024 * 1024),
                        "percent": process_memory.rss
                        / psutil.virtual_memory().total
                        * 100,
                    }
                )

                if process_io:
                    self.metrics["process_io_samples"].append(
                        {
                            "timestamp": time.time() - self.start_time,
                            "read_bytes": process_io.read_bytes,
                            "write_bytes": process_io.write_bytes,
                        }
                    )

                self.metrics["process_threads_samples"].append(
                    {
                        "timestamp": time.time() - self.start_time,
                        "threads": process_threads,
                    }
                )

                time.sleep(self.sampling_interval)

        except Exception as e:
            logger.error(f"Error in resource monitoring: {str(e)}")

    def _get_gpu_metrics(self) -> Dict[str, Any]:
        """Get GPU metrics if available"""
        metrics = {}

        # Try to get GPU metrics using pynvml (NVIDIA GPUs)
        try:
            import pynvml

            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()

            if device_count > 0:
                metrics["devices"] = []

                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    name = pynvml.nvmlDeviceGetName(handle)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

                    metrics["devices"].append(
                        {
                            "index": i,
                            "name": name,
                            "gpu_util_percent": util.gpu,
                            "memory_util_percent": util.memory,
                            "memory_used_mb": memory.used / (1024 * 1024),
                            "memory_total_mb": memory.total / (1024 * 1024),
                        }
                    )

        except (ImportError, Exception):
            # GPU monitoring not available or failed
            pass

        return metrics

    def stop_and_save(self):
        """Stop monitoring and save the collected metrics"""
        if not self.keep_monitoring:
            # Already stopped
            return

        self.keep_monitoring = False
        self.end_time = time.time()
        self.metrics["duration"] = self.end_time - self.start_time

        # Calculate peak and average values
        self._calculate_statistics()

        # Save metrics to file
        try:
            self._save_metrics()

            # Print summary to console
            self._print_summary_to_console()
            logger.debug(
                f"Resource metrics saved for {self.source_type} - {self.operation_type} "
                f"(Duration: {self.metrics['duration']:.2f}s)"
            )
        except Exception as e:
            logger.error(f"Failed to save resource metrics: {str(e)}")

    def _calculate_statistics(self):
        """Calculate peak and average values from samples"""
        # Process CPU statistics
        if self.metrics["process_cpu_samples"]:
            process_cpu_percents = [
                sample["percent"] for sample in self.metrics["process_cpu_samples"]
            ]
            self.metrics["peak_values"]["process_cpu_percent"] = (
                max(process_cpu_percents) if process_cpu_percents else 0
            )
            self.metrics["average_values"]["process_cpu_percent"] = (
                sum(process_cpu_percents) / len(process_cpu_percents)
                if process_cpu_percents
                else 0
            )

        # Process memory statistics
        if self.metrics["process_memory_samples"]:
            process_rss = [
                sample["rss_mb"] for sample in self.metrics["process_memory_samples"]
            ]
            process_vms = [
                sample["vms_mb"] for sample in self.metrics["process_memory_samples"]
            ]
            process_percent = [
                sample["percent"] for sample in self.metrics["process_memory_samples"]
            ]

            self.metrics["peak_values"]["process_memory_rss_mb"] = (
                max(process_rss) if process_rss else 0
            )
            self.metrics["peak_values"]["process_memory_vms_mb"] = (
                max(process_vms) if process_vms else 0
            )
            self.metrics["peak_values"]["process_memory_percent"] = (
                max(process_percent) if process_percent else 0
            )

            self.metrics["average_values"]["process_memory_rss_mb"] = (
                sum(process_rss) / len(process_rss) if process_rss else 0
            )
            self.metrics["average_values"]["process_memory_vms_mb"] = (
                sum(process_vms) / len(process_vms) if process_vms else 0
            )
            self.metrics["average_values"]["process_memory_percent"] = (
                sum(process_percent) / len(process_percent) if process_percent else 0
            )

        # Process I/O statistics (calculate totals from samples)
        if (
            self.metrics["process_io_samples"]
            and len(self.metrics["process_io_samples"]) > 1
        ):
            first_sample = self.metrics["process_io_samples"][0]
            last_sample = self.metrics["process_io_samples"][-1]

            self.metrics["total_process_read_mb"] = (
                last_sample["read_bytes"] - first_sample["read_bytes"]
            ) / (1024 * 1024)
            self.metrics["total_process_write_mb"] = (
                last_sample["write_bytes"] - first_sample["write_bytes"]
            ) / (1024 * 1024)

        # Process threads statistics
        if self.metrics["process_threads_samples"]:
            threads_counts = [
                sample["threads"] for sample in self.metrics["process_threads_samples"]
            ]
            self.metrics["peak_values"]["process_threads"] = (
                max(threads_counts) if threads_counts else 0
            )
            self.metrics["average_values"]["process_threads"] = (
                sum(threads_counts) / len(threads_counts) if threads_counts else 0
            )

    def _save_metrics(self):
        """Save metrics to a JSON file"""
        # Create a filename with timestamp, source type, and session ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{self.source_type}_{self.operation_type}_{self.session_id[:8]}.json"

        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2)

        # Also save a summary file with just the key metrics
        summary = {
            "session_id": self.session_id,
            "source_type": self.source_type,
            "operation_type": self.operation_type,
            "timestamp": self.metrics["timestamp"],
            "duration": self.metrics["duration"],
            "cpu_info": self.metrics.get("cpu_info", {}),  # Keep CPU hardware info
            "peak_values": self.metrics[
                "peak_values"
            ],  # Now contains only process metrics
            "average_values": self.metrics[
                "average_values"
            ],  # Now contains only process metrics
            "total_process_read_mb": self.metrics.get("total_process_read_mb", 0),
            "total_process_write_mb": self.metrics.get("total_process_write_mb", 0),
            "process_info": self.metrics.get("process_info", {}),
        }

        summary_filepath = (
            self.output_dir
            / f"{timestamp}_{self.source_type}_{self.operation_type}_{self.session_id[:8]}_summary.json"
        )

        with open(summary_filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    def _print_summary_to_console(self):
        """Print a summary of the resource metrics to the console"""
        # Create a formatted summary for console output
        console_summary = [
            f"\n{'=' * 50}",
            f" RESOURCE MONITORING SUMMARY - {self.source_type.upper()}",
            f"{'=' * 50}",
            f"Operation:      {self.operation_type}",
            f"Duration:       {self.metrics['duration']:.2f} seconds",
            f"Session ID:     {self.session_id[:8]}",
            f"\n--- CPU USAGE ---",
            f"Peak:           {self.metrics['peak_values'].get('process_cpu_percent', 0):.2f}%",
            f"Average:        {self.metrics['average_values'].get('process_cpu_percent', 0):.2f}%",
            f"\n--- MEMORY USAGE ---",
            f"Peak RSS:       {self.metrics['peak_values'].get('process_memory_rss_mb', 0):.2f} MB",
            f"Average RSS:    {self.metrics['average_values'].get('process_memory_rss_mb', 0):.2f} MB",
            f"Peak Memory %:  {self.metrics['peak_values'].get('process_memory_percent', 0):.2f}%",
            f"\n--- DISK I/O ---",
            f"Total Read:     {self.metrics.get('total_process_read_mb', 0):.2f} MB",
            f"Total Written:  {self.metrics.get('total_process_write_mb', 0):.2f} MB",
            f"\n--- THREADS ---",
            f"Peak Count:     {self.metrics['peak_values'].get('process_threads', 0)}",
            f"\nDetailed metrics saved to:",
            f"{self.output_dir}",
            f"{'=' * 50}\n",
        ]

        # Print the formatted summary
        logger.info("\n".join(console_summary))

        # Also log the summary
        logger.info(
            f"Resource monitoring completed for {self.source_type} - {self.operation_type}"
        )


def detect_source_type() -> str:
    """Detect the source of the invocation (git hook, vscode, github actions, or CLI)"""
    # Check for GitHub Actions environment variables
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return "github_actions"

    # Check for VS Code environment
    if os.environ.get("VSCODE_PID") or os.environ.get("VSCODE_CWD"):
        return "vscode"

    # Check for git hook - this is trickier, let's check command line or env
    if os.environ.get("GIT_HOOK") or (len(sys.argv) > 1 and "hooks" in sys.argv[0]):
        return "git_hook"

    # Default to CLI
    return "cli"


def start_monitoring(operation_type: str = "generate") -> ResourceMonitor:
    """
    Start monitoring resource usage

    Args:
        operation_type: The operation being performed (generate, configure, etc.)

    Returns:
        A ResourceMonitor instance
    """
    source_type = detect_source_type()
    return ResourceMonitor(source_type, operation_type)
