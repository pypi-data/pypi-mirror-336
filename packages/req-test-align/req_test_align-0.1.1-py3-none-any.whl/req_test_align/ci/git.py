import os
import subprocess
from typing import List, Optional, Dict

from ..types import ReviewFile
from ..utils.logger import logger
from ..utils.commit_utils import (
    parse_patch_content,
    extract_changed_components,
    do_patch,
)


def get_git_root() -> str:
    """Get the root directory of the Git repository"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Unable to find the git root directory. Error: {e.stderr}")


def get_changed_files_names(is_ci: Optional[str] = None) -> List[str]:
    """
    Get the names of the files with changes

    Args:
        is_ci: CI environment type

    Returns:
        List of file names
    """
    try:
        if is_ci == "github":
            # Get changed files from GitHub Actions
            base_ref = os.environ.get("GITHUB_BASE_REF")
            if base_ref:
                result = subprocess.run(
                    ["git", "diff", "--name-only", f"origin/{base_ref}...HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout.splitlines()

        # # Get unstaged files
        # unstaged_result = subprocess.run(
        #     ["git", "diff", "--name-only"], capture_output=True, text=True, check=True
        # )

        # Get staged files
        staged_result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Merge and deduplicate
        # all_files = set(
        #     unstaged_result.stdout.splitlines() + staged_result.stdout.splitlines()
        # )
        all_files = set(staged_result.stdout.splitlines())
        return list(all_files)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting changed files: {e.stderr}")
        return []


def get_file_content(file_path: str) -> str:
    """Get the content of the file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return ""


def get_file_diff(file_path: str, is_ci: Optional[str] = None) -> str:
    """Get the diff content of the file"""
    try:
        if is_ci == "github":
            # Get diff from GitHub Actions
            base_ref = os.environ.get("GITHUB_BASE_REF")
            if base_ref:
                result = subprocess.run(
                    ["git", "diff", f"origin/{base_ref}...HEAD", "--", file_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout
        # Check if the file is staged
        staged_result = subprocess.run(
            ["git", "diff", "--cached", "--", file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        # If the file is staged, return the staged diff
        if staged_result.stdout:
            return staged_result.stdout

        return ""
        # # Otherwise, return the unstaged diff
        # unstaged_result = subprocess.run(
        #     ["git", "diff", "--", file_path], capture_output=True, text=True, check=True
        # )
        # return unstaged_result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting diff for file {file_path}: {e.stderr}")
        return ""


async def get_files_with_changes(is_ci: Optional[str] = None) -> List[ReviewFile]:
    """
    Get files with changes

    Args:
        is_ci: CI environment type

    Returns:
        List of files with changes
    """
    try:
        git_root = get_git_root()
        changed_files = get_changed_files_names(is_ci)

        if not changed_files:
            return []

        result = []
        for file_name in changed_files:
            file_path = os.path.join(git_root, file_name)

            if os.path.exists(file_path):
                file_content = get_file_content(file_path)
                changed_content = get_file_diff(file_path, is_ci)
                parsed_changes = parse_patch_content(
                    file_name, changed_content.splitlines()
                )

                functions_before, test_cases_before = extract_changed_components(
                    file_path,
                    file_content,
                    parsed_changes,
                    to_get_bugs=True,
                    language="python",
                    function_only=False,
                )

                patched_file_content = do_patch(file_content, changed_content)
                functions_after, test_cases_after = extract_changed_components(
                    file_path,
                    patched_file_content,
                    parsed_changes,
                    to_get_bugs=False,
                    language="python",
                    function_only=False,
                )

                result.append(
                    {
                        "fileName": file_name,
                        "fileContent": file_content,
                        "changedContent": changed_content,
                        "parsedChanges": parsed_changes,
                        "functions_after": functions_after,
                        "functions_before": functions_before,
                        "testCases_after": test_cases_after,
                        "testCases_before": test_cases_before,
                    }
                )
        return result
    except Exception as e:
        logger.error(f"Error getting files with changes: {str(e)}")
        return []
