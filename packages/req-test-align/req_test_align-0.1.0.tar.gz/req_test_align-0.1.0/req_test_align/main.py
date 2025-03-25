import asyncio
import os
import sys
from typing import List, Optional

from .types import ReviewFile
from .utils.logger import logger
from .utils.utils import get_args
from .config import openai_api_key, openai_host
from .core.align_test_case import generate_aligned_test_cases
from .configure import configure
from .ci.git import get_files_with_changes
from .ci.github import get_remote_pull_request_files
from .monitor import start_monitoring


async def get_changed_files(
    is_ci: Optional[str] = None, remote_pull_request: Optional[str] = None
) -> List[ReviewFile]:
    """
    Get files to align

    Args:
        is_ci: CI environment type
        remote_pull_request: Remote pull request URL or identifier

    Returns:
        List of files to align
    """
    if remote_pull_request:
        return await get_remote_pull_request_files(remote_pull_request)

    return await get_files_with_changes(is_ci)


async def main():
    """
    Main function
    """
    # Start resource monitoring
    monitor = start_monitoring("generate")

    args = get_args()

    if args["command"] == "configure":
        await configure(args["setupTarget"])
        return

    if args["command"] == "generate":
        api_key = openai_api_key()
        api_host = openai_host()
        if not api_key:
            logger.error(
                "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
            )
            sys.exit(1)

        files = await get_changed_files(args["ci"], args["remote"])

        if not files:
            logger.info("No files to align.")
            return

        result = await generate_aligned_test_cases(
            args, files, api_key, api_host, requirement=args["requirement"]
        )

        if result:
            logger.debug("Aligned test cases successfully generated.")
            print("\n" + result)  # Display aligned test case in console
        else:
            logger.debug("No aligned test cases were generated.")

        monitor.stop_and_save()

        return

    logger.error(f"Unknown command: {args['command']}")
    sys.exit(1)


def main_entry():
    """Command line entry point"""
    asyncio.run(main())
