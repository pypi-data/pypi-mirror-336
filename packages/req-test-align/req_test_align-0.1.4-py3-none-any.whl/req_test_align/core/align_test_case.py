import os
import parso
from pathlib import Path
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..types import ReviewArgs, ReviewFile
from ..config import SIGN_OFF
from ..utils.logger import logger
from ..utils.utils import filter_files, get_max_prompt_length
from .ai_client import (
    construct_test_case_generation_prompt,
    generate_requirement_msg,
    construct_requirement_generation_prompt,
    generate_test_cases,
    construct_judge_alignment_prompt,
    get_aligned_test_cases,
)
from ..ci.github import comment_on_pr, comment_per_file


async def generate_aligned_test_cases(
    args: ReviewArgs,
    files: List[ReviewFile],
    openai_api_key: str,
    openai_host: str,
    requirement: str = None,
) -> Optional[str]:
    """
    Perform code generation.

    Args:
        args: Generation arguments.
        files: List of files.
        openai_api_key: OpenAI API key.
        openai_host: OpenAI host.
        requirement: Requirement to generate test cases for.

    Returns:
        Generation report.
    """
    logger.debug("Generation started.")
    logger.debug(f"Requirement: {requirement or 'Requirement not defined'}")
    logger.debug(f"Model used: {args['model']}")
    logger.debug(f"CI enabled: {args['ci'] or 'CI not defined'}")
    # logger.debug(f"Comment per file enabled: {str(args['commentPerFile'])}")
    logger.debug(f"Selected generation type: {args['reviewType']}")
    logger.debug(f"Selected organization: {args['org'] or 'Organization not defined'}")
    logger.debug(
        f"Remote Pull Request: {args['remote'] or 'Remote pull request not defined'}"
    )

    is_ci = args["ci"]
    # should_comment_per_file = args["commentPerFile"]
    model_name = args["model"]
    review_type = args["reviewType"]
    organization = args["org"]

    generation_language = args["review_language"]
    test_affected = args["testAffected"]
    test_target = args["testTarget"]

    filtered_files = filter_files(files)

    if not filtered_files:
        logger.info("No files to align, completing alignment now.")
        return None

    logger.debug(
        f"Files to align after filtering: {', '.join(file['fileName'] for file in filtered_files)}"
    )

    max_prompt_length = get_max_prompt_length(model_name)

    # 1. Get the requirement
    if not requirement:
        requirement_prompt = construct_requirement_generation_prompt(
            filtered_files, max_prompt_length, review_type, generation_language
        )
        requirement = await generate_requirement_msg(
            requirement_prompt,
            model_name,
            openai_api_key,
            openai_host,
            organization,
        )

    # 2. Get the test cases
    test_files = construct_target_test_files(filtered_files, test_affected, test_target)

    logger.debug(
        f"Test files to align: {', '.join(file['fileName'] for file in test_files)}"
    )

    test_file_names = [file["fileName"] for file in test_files]

    function_files = []
    for filtered_file in filtered_files:
        if filtered_file["fileName"] not in test_file_names:
            function_files.append(filtered_file)

    test_cases = extract_test_cases(test_files)

    judge_alignment_prompt = construct_judge_alignment_prompt(
        requirement, function_files, test_cases, max_prompt_length
    )

    aligned_test_cases = await get_aligned_test_cases(
        judge_alignment_prompt, model_name, openai_api_key, openai_host, organization
    )

    aligned_pairs = set(
        (entry["file"], testcase["test_name"])
        for entry in aligned_test_cases
        for testcase in entry["testcases"]
    )

    unaligned_test_cases = [
        test
        for test in test_cases
        if (test["file_name"], test["test_name"]) not in aligned_pairs
    ]

    logger.debug(
        f"Number of Aligned test cases: {len(aligned_test_cases)}, Number of Unaligned test cases: {len(unaligned_test_cases)}, Total test cases: {len(test_cases)}"
    )

    generation_prompt = construct_test_case_generation_prompt(
        function_files,
        test_files,
        max_prompt_length,
        review_type,
        generation_language,
        requirement,
        to_judge_alignment=False,
        aligned_test_cases=aligned_test_cases,
        unaligned_test_cases=unaligned_test_cases,
    )

    markdown_report, feedbacks = await generate_test_cases(
        generation_prompt, model_name, openai_api_key, openai_host, organization
    )

    # If running in GitHub CI environment
    if is_ci == "github":
        # todo: add comment per file
        await comment_on_pr(markdown_report, SIGN_OFF)

    return markdown_report


def construct_target_test_files(
    filtered_files: Optional[List[Dict[str, Any]]] = None,
    test_affected: bool = False,
    test_target: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """
    Constructs a list of test case files based on specified parameters.

    The function follows these rules:
    1. If test_target is provided: Process files/directories in the list, collecting
       files that match test naming conventions (starts with 'test_' or ends with '_test.py').
    2. else: Scan current directory recursively for test files.

    Args:
        filtered_files: List of files that were modified
        test_affected: Whether to run tests on affected files only
        test_target: List of target test files or directories

    Returns:
        List of dictionaries containing test file names and their content
    """
    result = []

    if test_target:
        result = _get_test_files_from_targets(
            filtered_files, test_target, test_affected
        )
    else:
        result = _get_all_test_files(filtered_files, test_affected)

    return result


def _extract_modified_functions(filtered_files: List[Dict[str, Any]]):
    """
    Extract modified functions and filenames from the filtered files.

    Args:
        filtered_files: List of modified files with their content/diff information

    Returns:
        Tuple containing modified functions

    """
    modified_functions = set()
    modified_filenames = set()

    for file in filtered_files:
        if (
            "fileName" not in file
            or len(file.get("functions_after", {}).keys()) == 0
            and len(file.get("functions_before", {}).keys()) == 0
        ):
            continue

        file_path = file["fileName"]
        modified_filenames.add(file_path)

        # Extract function names from functions_after/before
        if "functions_after" in file:
            for filepath, functions in file["functions_after"].items():
                for func in functions:
                    modified_functions.add(func["name"])

        # If we couldn't extract from functions_after, try to parse from changedContent
        if "changedContent" in file and not modified_functions:
            diff_content = file["changedContent"]
            # Simple heuristic to find function definitions in diff
            for line in diff_content.split("\n"):
                if line.startswith("+") and "def " in line:
                    # Extract function name from 'def function_name('
                    func_part = line.split("def ")[1].split("(")[0].strip()
                    modified_functions.add(func_part)

    logger.debug(
        f"Modified functions detected: {', '.join(modified_functions) if modified_functions else 'None'}"
    )
    logger.debug(
        f"Modified files detected: {', '.join(modified_filenames) if modified_filenames else 'None'}"
    )

    return modified_functions, modified_filenames


def _get_affected_test_files(test_files, modified_functions, modified_filenames):
    """
    Get relevant test files based on modified functions and filenames.

    Args:
        test_files: List of test files
        modified_functions: Set of modified functions
        modified_filenames: Set of modified filenames

    Returns:
        List of relevant test files
    """
    relevant_test_files = []
    for test_file in test_files:
        content = test_file["fileContent"]

        # Check if the test file imports from any of the modified files
        is_relevant = False

        # Check if test file imports any modified files
        for filename in modified_filenames:
            # Convert file path to module format in a cross-platform way
            module_name = os.path.splitext(filename)[0]
            module_name = module_name.replace(os.sep, ".")
            # Also try with forward slashes for import compatibility
            alternative_module_name = os.path.splitext(filename)[0].replace("/", ".")

            if module_name in content or alternative_module_name in content:
                is_relevant = True
                break

        # Check if test file references any modified functions
        if not is_relevant:
            for func_name in modified_functions:
                if func_name in content:
                    is_relevant = True
                    break

        if is_relevant:
            relevant_test_files.append(test_file)

    # If we found relevant test files, use them; otherwise return all test files
    if relevant_test_files:
        logger.debug(f"Found {len(relevant_test_files)} relevant test files")
        result = relevant_test_files
    else:
        # If no test files were deemed relevant, return all test files
        logger.debug("No specific relevant test files found, returning all test files")
        result = test_files

    return result


def _get_test_files_from_targets(
    filtered_files: Optional[List[Dict[str, Any]]] = None,
    test_target: Optional[List[str]] = None,
    test_affected: bool = False,
) -> List[Dict[str, str]]:
    """
    Process specified test targets to find test files.

    Args:
        filtered_files: List of modified files with their content/diff information
        test_target: List of target test files or directories
        test_affected: Whether to filter for affected test files

    Returns:
        List of dictionaries containing test file information
    """
    result = []
    processed_files = set()

    if not test_target:
        return result

    for target in test_target:
        path = Path(target)
        if not path.exists():
            logger.debug(f"Test target does not exist: {target}")
            continue

        if path.is_file() and _is_test_file(path.name):
            # Target is a test file
            if path.name not in processed_files:
                result.append(_read_test_file(path))
                processed_files.add(path.name)
        elif path.is_dir():
            # Target is a directory, find all test files within
            for test_file in path.glob("**/*"):
                if (
                    test_file.is_file()
                    and test_file.name not in processed_files
                    and _is_test_file(test_file.name)
                ):
                    result.append(_read_test_file(test_file))
                    processed_files.add(test_file.name)

    # If test_affected is True, filter the results to only include affected test files
    if test_affected and filtered_files:
        modified_functions, modified_filenames = _extract_modified_functions(
            filtered_files
        )
        return _get_affected_test_files(result, modified_functions, modified_filenames)

    return result


def _get_all_test_files(filtered_files, test_affected) -> List[Dict[str, str]]:
    """
    Find all test files in the current directory and subdirectories.

    Returns:
        List of dictionaries containing test file information
    """
    modified_functions, modified_filenames = _extract_modified_functions(filtered_files)

    current_test_files = {}
    for file in filtered_files:
        # Use os.path.basename instead of string split for cross-platform compatibility
        if _is_test_file(os.path.basename(file["fileName"])):
            current_test_files[file["fileName"]] = {
                "fileName": file["fileName"],
                "fileContent": file["fileContent"],
            }

    result = []

    for root, _, files in os.walk("."):
        for filename in files:
            if _is_test_file(filename):
                # Use os.path.normpath to ensure proper path format for the current OS
                file_path = os.path.normpath(os.path.join(root, filename))
                # Remove leading ./ or .\ in a cross-platform way
                if file_path.startswith("." + os.sep):
                    file_path = file_path[2:]

                if file_path in current_test_files:
                    result.append(current_test_files[file_path])
                else:
                    result.append(_read_test_file(Path(file_path)))

    return (
        _get_affected_test_files(result, modified_functions, modified_filenames)
        if test_affected
        else result
    )


def _is_test_file(filename: str) -> bool:
    """
    Check if a file is a test file based on naming convention.

    Args:
        filename: Name of the file to check

    Returns:
        True if the file is a test file, False otherwise
    """
    return filename.endswith(".py") and (
        filename.startswith("test_") or filename.endswith("_test.py")
    )


def _read_test_file(file_path: Path) -> Dict[str, str]:
    """
    Read a test file and return its information.

    Args:
        file_path: Path to the test file

    Returns:
        Dictionary containing file name and content
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Convert Path object to string in a cross-platform way
            return {
                "fileName": str(file_path).replace("\\", "/"),
                "fileContent": f.read(),
            }
    except Exception as e:
        logger.debug(f"Error reading test file {file_path}: {str(e)}")
        return {"fileName": str(file_path).replace("\\", "/"), "fileContent": ""}


def extract_test_cases(test_files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Extract test cases from Python test files.

    Args:
        test_files: List of dictionaries containing test file information
                   Each dictionary should have 'fileName' and 'fileContent' keys

    Returns:
        List of dictionaries containing test case information:
        {
            'file_name': str,           # File name containing the test
            'test_name': str,           # Test function name
            'line_number': int,         # Line number where the test starts
            'code': str,                # Full test function code
            'docstring': Optional[str], # Docstring of the test (if any)
            'assertions': List[str]     # List of assertion statements in the test
        }
    """
    all_test_cases = []

    for test_file in test_files:
        file_name = test_file["fileName"]
        content = test_file["fileContent"]

        # Parse the file content
        module = parso.parse(content)

        # Extract test functions from the file
        test_cases = _extract_test_functions_from_module(module, file_name)
        all_test_cases.extend(test_cases)

    return all_test_cases


def _extract_test_functions_from_module(module, file_name: str) -> List[Dict[str, Any]]:
    """
    Extract test functions from a parsed module.

    Args:
        module: parso parsed module
        file_name: Name of the file being processed

    Returns:
        List of dictionaries containing test case information
    """
    test_cases = []

    # Find all classes and functions in the module
    for node in module.children:
        # If it's a class definition (possibly a test class)
        if node.type == "classdef":
            class_name = node.name.value

            # Check if it's a test class (starts with 'Test')
            if class_name.startswith("Test"):
                # Extract test methods from the class
                test_methods = _extract_test_methods_from_class(
                    node, file_name, class_name
                )
                test_cases.extend(test_methods)

        # If it's a function at module level (possibly a test function)
        elif node.type == "funcdef":
            func_name = node.name.value

            # Check if it's a test function (starts with 'test_')
            if func_name.startswith("test_"):
                test_info = _extract_test_info(node, file_name, None, func_name)
                if test_info:
                    test_cases.append(test_info)

    return test_cases


def _extract_test_methods_from_class(
    class_node, file_name: str, class_name: str
) -> List[Dict[str, Any]]:
    """
    Extract test methods from a test class.

    Args:
        class_node: parso class node
        file_name: Name of the file being processed
        class_name: Name of the class

    Returns:
        List of dictionaries containing test method information
    """
    test_methods = []

    # Find the class body (usually a suite node)
    for child in class_node.children:
        if child.type == "suite":
            # Iterate through class body elements
            for node in child.children:
                # If it's a function definition (method)
                if node.type == "funcdef":
                    method_name = node.name.value

                    # Check if it's a test method (starts with 'test_')
                    if method_name.startswith("test_"):
                        test_info = _extract_test_info(
                            node, file_name, class_name, method_name
                        )
                        if test_info:
                            test_methods.append(test_info)

    return test_methods


def _extract_test_info(
    func_node, file_name: str, class_name: Optional[str], func_name: str
) -> Dict[str, Any]:
    """
    Extract information from a test function/method.

    Args:
        func_node: parso function node
        file_name: Name of the file being processed
        class_name: Name of the class (None if it's a function)
        func_name: Name of the function

    Returns:
        Dictionary containing test information
    """
    # Get line number
    line_number = func_node.start_pos[0]

    # Get function code
    code = func_node.get_code()

    # Initialize docstring and assertions
    docstring = None
    assertions = []

    # Find function body (usually a suite node)
    for child in func_node.children:
        if child.type == "suite":
            # First statement might be a docstring
            if child.children and child.children[0].type == "simple_stmt":
                first_stmt = child.children[0]
                if first_stmt.children and first_stmt.children[0].type == "string":
                    docstring = first_stmt.children[0].value

            # Extract assertions from function body
            assertions = _extract_assertions(child)

    # Create full qualified name
    if class_name:
        full_name = f"{class_name}.{func_name}"
    else:
        full_name = func_name

    return {
        "file_name": file_name,
        "test_name": full_name,
        "line_number": line_number,
        "code": code,
        "docstring": docstring,
        "assertions": assertions,
    }


def _extract_assertions(node) -> List[str]:
    """
    Recursively extract assertion statements from a node.

    Args:
        node: parso node to extract assertions from

    Returns:
        List of assertion statements
    """
    assertions = []

    if hasattr(node, "children"):
        for child in node.children:
            # If it's a simple statement that might contain an assertion
            if child.type == "simple_stmt":
                for subchild in child.children:
                    if subchild.type == "expr_stmt":
                        # Look for method calls that might be assertions
                        if _is_assertion(subchild):
                            assertions.append(subchild.get_code().strip())

            # Recursively check child nodes
            assertions.extend(_extract_assertions(child))

    return assertions


def _is_assertion(node) -> bool:
    """
    Check if a node represents an assertion.

    Args:
        node: parso node to check

    Returns:
        True if the node represents an assertion, False otherwise
    """
    # Look for 'assert' statements
    if node.type == "assert_stmt":
        return True

    code = node.get_code().strip()

    # Check for pytest style assertions (like assert_equal, assert_true, etc.)
    assertion_prefixes = [
        "assert ",
        "self.assert",
        "assert_",
        "assertRaises",
        "assertAlmostEqual",
        "assertEqual",
        "assertTrue",
        "assertFalse",
        "assertIn",
        "assertNotIn",
    ]

    return any(code.startswith(prefix) for prefix in assertion_prefixes)
