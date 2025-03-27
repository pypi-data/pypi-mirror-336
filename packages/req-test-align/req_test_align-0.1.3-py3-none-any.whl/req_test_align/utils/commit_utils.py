import re
import subprocess
from .java_utils import extract_code_structure_java
from .python_utils import extract_code_structure_python
from unidiff import PatchSet


def parse_patch_content(file, patch_content):
    """
    Parse the patch content and extract the changes.

    Args:
        file: File name
        patch_content: Patch content as a list of lines

    Returns:
        list: List of changes in the patch
    """
    changes = []

    for line in patch_content:
        # Check for hunk headers
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@", line)
            if match and file is not None:
                old_start = int(match.group(1))
                old_lines = int(match.group(2) or 1)
                new_start = int(match.group(3))
                new_lines = int(match.group(4) or 1)
                changes.append(
                    {
                        "file": file,
                        "old_start": old_start,
                        "old_end": old_start + old_lines - 1,
                        "new_start": new_start,
                        "new_end": new_start + new_lines - 1,
                    }
                )
    return changes


def do_patch(original_text, patch_text, file_path="", reverse=False):
    """
    Apply patch to original text using unidiff.

    Args:
        original_text: Original text content as a string
        patch_text: Unified diff format patch as a string
        file_path: Path of the file to apply the patch to. Default is "" (apply to all files).
        reverse: If True, reverse the patch (unapply it). Default is False.

    Returns:
        str: Text content after applying/reversing the patch
    """
    # Split the original text into lines
    original_lines = original_text.splitlines()  # Keep line endings

    # Parse the patch
    patch = PatchSet(patch_text)

    # For each file in the patch (usually just one in text patching)
    for patched_file in patch:
        if file_path and patched_file.path != file_path:
            continue
        # Track line offsets as we apply hunks
        line_offset = 0

        # Get hunks in reverse order if we're reversing the patch
        hunks = list(patched_file)
        if reverse:
            hunks.reverse()

        # Apply each hunk
        for hunk in hunks:
            if reverse:
                # When reversing, we swap source and target
                actual_start = hunk.target_start - 1 + line_offset
                actual_length = hunk.target_length
                new_length = hunk.source_length
            else:
                actual_start = hunk.source_start - 1 + line_offset
                actual_length = hunk.source_length
                new_length = hunk.target_length

            # Get the parts before and after the hunk
            before = original_lines[:actual_start]
            after = original_lines[actual_start + actual_length :]

            # Get the new lines from the hunk
            new_lines = []
            for line in hunk:
                if reverse:
                    # When reversing, we keep removed lines and skip added lines
                    if not line.is_added:  # Keep context lines and removed lines
                        new_lines.append(line.value)
                else:
                    # Normal application keeps context and added lines
                    if not line.is_removed:
                        new_lines.append(line.value)

            # Update the original lines with the patched content
            original_lines = before + new_lines + after

            # Update offset for subsequent hunks
            line_offset += new_length - actual_length

    # Join the lines back into a string
    result = "".join(original_lines)
    return result


def extract_changed_components(
    file_path,
    file_content,
    changes,
    to_get_bugs=False,
    language="java",
    function_only=False,
):
    """
    Apply the commit and extract the code structure.

    Args:
        file_path: Path of the file
        file_content: Content of the file
        changes: List of changed files and their modifications
        to_get_bugs: Flag to get buggy or fixed commit
        language: Programming language of the code
        function_only: Whether to extract only function/method definitions

    Returns:
        tuple: (function_codes, test_cases)
    """
    extracted_data = {}
    test_paths = ["test/", "tests/"]

    try:
        extracted_data = extract_functions_and_classes_by_patch(
            file_path,
            file_content,
            changes,
            to_get_old_lines=to_get_bugs,
            language=language,
            function_only=function_only,
        )
    except Exception as e:
        print(f"Error extracting code: {e}")

    # Separate function code and test cases
    function_codes, test_cases = {}, {}
    for path, data in extracted_data.items():
        if any(test_path in path for test_path in test_paths):
            test_cases[path] = data
        else:
            function_codes[path] = data

    return function_codes, test_cases


def extract_functions_and_classes_by_patch(
    file_path,
    file_content,
    changes,
    to_get_old_lines=False,
    language="java",
    function_only=False,
):
    """
    Extract the complete code structure of the changed files.

    Args:
        file_path: Path of the file
        file_content: Content of the file
        changes: List of changed files and their modifications
        to_get_old_lines: Flag to get old or new lines
        language: Programming language of the code
        function_only: Whether to extract only function/method definitions

    Returns:
        dict: Extracted code structure of the changed files
              {file_path: [{type: str, code: str, start_line: int, end_line: int}, ...]}
    """
    extracted_data = {}
    for change in changes:
        # Determine which lines to consider based on whether we want old or new lines
        if to_get_old_lines:
            code_start_line, code_end_line = (
                change["old_start"],
                change["old_end"],
            )
        else:
            code_start_line, code_end_line = (
                change["new_start"],
                change["new_end"],
            )

        # Extract code structure based on language
        try:
            if language == "java":
                result = extract_code_structure_java(
                    file_content, code_start_line, code_end_line
                )
            elif language == "python":
                result = extract_code_structure_python(
                    file_content,
                    code_start_line,
                    code_end_line,
                    function_only=function_only,
                )
            else:
                result = None

            # Add result to extracted data if available
            if result:
                if file_path in extracted_data:
                    extracted_data[file_path].update(result)
                else:
                    extracted_data[file_path] = result

        except Exception as e:
            print(f"Error extracting code structure from {file_path}: {e}")
    # Convert the extracted data to list format
    for path, data in extracted_data.items():
        extracted_data[path] = list(data.values())

    return extracted_data
