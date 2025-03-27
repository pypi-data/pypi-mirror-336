import os
import argparse
from typing import List

from ..types import ReviewArgs, ReviewFile, TestFile
from .logger import logger
from ..config import LANGUAGE_MAP, SUPPORTED_FILES, EXCLUDED_KEYWORDS, MODEL_INFO


def get_args() -> ReviewArgs:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Requirements-test align")
    subparsers = parser.add_subparsers(
        dest="command", help="Command to run", required=True
    )

    # Configure command
    configure_parser = subparsers.add_parser("configure", help="Configure the tool")
    configure_parser.add_argument(
        "--setupTarget",
        choices=["github", "local"],
        help="Specify which platform to configure the project for",
        default="github",
    )

    # Review command
    review_parser = subparsers.add_parser("generate", help="Review code changes")
    review_parser.add_argument(
        "--ci", choices=["github"], help="CI environment type", default=None
    )
    # review_parser.add_argument(
    #     "--commentPerFile",
    #     action="store_true",
    #     help="Enable per-file feedback. Only works when the script runs on GitHub.",
    #     default=False,
    # ) # todo: remove this
    review_parser.add_argument(
        "--model", help="Model to use for generating reviews.", default="gpt-4o-mini"
    )
    review_parser.add_argument(
        "--reviewType",
        choices=["full", "changed", "costOptimized"],
        help="Type of review to perform.",
        default="changed",
    )
    review_parser.add_argument(
        "--review_language",
        help="Specify target natural language for translation",
        default="English",
    )
    review_parser.add_argument(
        "--remote", help="Identifier of remote Pull Request to review", default=None
    )
    review_parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging.", default=False
    )
    review_parser.add_argument("--org", help="Organization ID for openAI", default=None)
    review_parser.add_argument(
        "--provider", choices=["openai"], help="Provider for AI", default="openai"
    )
    review_parser.add_argument(
        "--requirement",
        help="Requirement to generate test cases for",
        default=None,
    )

    review_parser.add_argument(
        "--testAffected",
        action="store_true",
        help="Generate test cases for affected files only",
        default=False,
    )

    review_parser.add_argument(
        "--testTarget",
        help="Specify the list of file or directory to run pytest on",
        nargs="+",
        default=[],
    )

    args = parser.parse_args()

    # Set log level
    if hasattr(args, "debug") and args.debug:
        logger.set_debug(True)

    # Convert to ReviewArgs type
    review_args = vars(args)

    return review_args


def find_template_file(pattern: str) -> str:
    """
    Find template file

    Args:
        pattern: File name pattern

    Returns:
        Template file path
    """
    # First look in current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, "templates")

    # Ensure the templates directory exists
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir, exist_ok=True)

    # Find matching files
    file_name = os.path.basename(pattern.replace("**/", ""))
    template_path = os.path.join(templates_dir, file_name)

    if os.path.exists(template_path):
        return template_path

    # Raise error if template not found
    raise FileNotFoundError(f"Template file not found: {pattern}")


def get_language_name(file_name: str) -> str:
    """
    Get programming language name based on file name

    Args:
        file_name: File name

    Returns:
        Programming language name
    """
    _, file_extension = os.path.splitext(file_name)

    if file_extension in LANGUAGE_MAP:
        return LANGUAGE_MAP[file_extension]

    return "Unknown"


def filter_files(files: List[ReviewFile]) -> List[ReviewFile]:
    """
    Filter file list, keeping only supported file types

    Args:
        files: File list

    Returns:
        Filtered file list
    """
    filtered_files = []

    for file in files:
        _, file_extension = os.path.splitext(file["fileName"])

        # Check if file extension is supported
        if file_extension in SUPPORTED_FILES:
            # Check if file name contains excluded keywords
            should_exclude = False
            for keyword in EXCLUDED_KEYWORDS:
                if keyword in file["fileName"].lower():
                    should_exclude = True
                    break

            if not should_exclude:
                filtered_files.append(file)

    return filtered_files


def get_max_prompt_length(model_name: str) -> int:
    """
    Get maximum prompt length for the model

    Args:
        model_name: Model name

    Returns:
        Maximum prompt length
    """
    # Look up model info
    for model in MODEL_INFO:
        if model["model"] == model_name:
            return model["maxPromptLength"]

    # Default value
    return 9000  # Approximately 4k tokens


def has_intersection_between_code_lines(section1, section2):
    """
    Check if two code sections have intersection.
    """
    return max(section1[0], section2[0]) <= min(section1[1], section2[1])


def genreate_test_case_report(test_files: List[TestFile]) -> str:
    """
    Generate test case report.

    Args:
        test_cases: List of test cases

    Returns:
        Test case report
    """
    md_lines = ["# Test Report\n"]

    for test_file in test_files:
        md_lines.append(f"## File: {test_file.get('file')}\n")
        for test in test_file["testcases"]:

            md_lines.append(
                f"  - **Line**: {'' if not test.get('start_line') or test.get('start_line') == test.get('line') else str(test.get('start_line')) + '-'}{test.get('line')}"
            )
            if test.get("previous"):
                md_lines.append(f"  - **Current test case**:")
                # Add code block
                md_lines.append("```")
                md_lines.append(test.get("previous"))
                md_lines.append("```")

            md_lines.append(f"  - **Status**: {test.get('status')}")

            if test.get("status") and test.get("status").lower() == "outdated":
                if test.get("added") == "1":
                    md_lines.append(f"  - **Should change**: Yes")
                else:
                    md_lines.append(f"  - **Should remove**: Yes")
            elif test.get("added") == "1":
                md_lines.append(f"  - **Should add**: Yes")

            if test.get("testcase"):
                md_lines.append(f"  - **New test case**:")
                # Add code block
                md_lines.append("```")
                md_lines.append(test.get("testcase"))
                md_lines.append("```")
            md_lines.append(f"  - **Reason**: {test.get('reason')}")
            md_lines.append("---")

    return "\n".join(md_lines)


def generate_general_markdown_report(data, level=1, dict_list_level=None):
    """
    Convert JSON data to a formatted Markdown string.

    Args:
        data: JSON data
        level: Heading level
        dict_list_level: Dictionary list level
    Returns:
        Markdown string
    """
    md = ""

    # If data is a dictionary, iterate over the keys and write them as headings in Markdown.
    if isinstance(data, dict):
        for key in data:
            md += f"{'#' * level} {key}\n\n"
            md += generate_general_markdown_report(
                data[key], level + 1, dict_list_level
            )

    # If data is a list, iterate over the items and write them in Markdown.
    # If the items are dictionaries, write an integer heading for each item and call the function recursively.
    elif isinstance(data, list):
        dict_list_level = level + 1

        for iitem, item in enumerate(data):
            if isinstance(item, dict):
                if level != 0:
                    md += "---\n\n"
                    md += f"{'#' * dict_list_level} Item {iitem}\n\n"
                    md += "---\n\n"
                md += generate_general_markdown_report(
                    item, dict_list_level + 1, dict_list_level
                )
            else:
                md += f"- {item}\n"

        md += "\n"

    else:
        md += f"{data}\n\n"

    return md
