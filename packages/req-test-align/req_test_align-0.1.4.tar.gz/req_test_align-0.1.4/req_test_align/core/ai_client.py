import json
from openai import OpenAI
from typing import Dict, List, Optional

from ..types import PromptFile, ReviewFile, TestFile
from ..utils.logger import logger
from ..utils.utils import get_language_name, genreate_test_case_report
from ..config import (
    INSTRUCTION_PROMPT,
    MAX_SURROUNDING_LINES,
    REQUIREMENT_GENERATION_PROMPT,
    TEST_CASE_GENERATION_PROMPT_PREFIX,
    TEST_CASE_GENERATION_PROMPT,
    JUDGE_ALIGNMENT_PROMPT,
    ALIGNED_TEST_CASE_GENERATION_PROMPT,
)


async def ask_ai(
    prompts: List[str],
    model_name: str,
    api_key: str,
    api_host: Optional[str] = None,
    organization: Optional[str] = None,
):
    """
    Ask the AI model for feedback.

    Args:
        prompts: List of prompts.
        model_name: Model name.
        api_key: API key.
        api_host: API host.
        organization: Organization ID (optional).
        generate_report: Generate a markdown report.

    Returns:
        AI response.
    """
    # Set up the OpenAI client
    client = OpenAI(
        api_key=api_key,
        base_url=api_host if api_host else None,
        organization=organization,
    )

    all_feedbacks = []

    # Process each prompt
    for prompt in prompts:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at software engineering and requirement engineering.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )

            content = response.choices[0].message.content

            # remove the ```json``` part
            content = content.replace("```json", "").replace("```", "")

            if content:
                parsed_response = json.loads(content)

                # Extract feedbacks
                if isinstance(parsed_response, list):
                    for feedback in parsed_response:
                        all_feedbacks.append(feedback)
                elif isinstance(parsed_response, dict):
                    all_feedbacks.append(parsed_response)

        except Exception as e:
            logger.error(f"Error when processing the prompts: {str(e)}")

    return all_feedbacks


def get_length_of_file(file: PromptFile) -> int:
    """
    Get the length of a file (filename length + prompt content length).

    Args:
        file: Prompt file.

    Returns:
        Total file length.
    """
    return len(file["fileName"]) + len(file["promptContent"])


def full_files_into_batches(
    files: List[ReviewFile], max_prompt_payload_length: int
) -> List[List[PromptFile]]:
    """
    Batch full file content, ensuring each batch does not exceed the maximum prompt length.

    Args:
        files: List of files.
        max_prompt_payload_length: Maximum prompt payload length.

    Returns:
        List of batched prompt files.
    """
    batches: List[List[PromptFile]] = []
    current_batch: List[PromptFile] = []
    current_batch_length = 0

    for file in files:
        prompt_file = {
            "fileName": file["fileName"],
            "promptContent": file["fileContent"],
            "changedContent": file["changedContent"],
        }

        file_length = get_length_of_file(prompt_file)

        # Start a new batch if adding this file would exceed the max length
        if current_batch_length + file_length > max_prompt_payload_length:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_batch_length = 0

        current_batch.append(prompt_file)
        current_batch_length += file_length

    # Add the last batch
    if current_batch:
        batches.append(current_batch)

    return batches


def changed_lines_into_batches(
    files: List[ReviewFile], max_prompt_payload_length: int
) -> List[List[PromptFile]]:
    """
    Batch changed lines, ensuring each batch does not exceed the maximum prompt length.

    Args:
        files: List of files.
        max_prompt_payload_length: Maximum prompt payload length.

    Returns:
        List of batched prompt files.
    """
    batches: List[List[PromptFile]] = []
    current_batch: List[PromptFile] = []
    current_batch_length = 0

    for file in files:
        # Use changed lines if available, otherwise use full file content
        content = (
            file["changedContent"] if file["changedContent"] else file["fileContent"]
        )

        prompt_file = {"fileName": file["fileName"], "promptContent": content}

        file_length = get_length_of_file(prompt_file)

        # Start a new batch if adding this file would exceed the max length
        if current_batch_length + file_length > max_prompt_payload_length:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_batch_length = 0

        current_batch.append(prompt_file)
        current_batch_length += file_length

    # Add the last batch
    if current_batch:
        batches.append(current_batch)

    return batches


def extract_changed_lines_with_context(diff_content: str, context_lines: int) -> str:
    """
    Extract changed lines from diff content along with surrounding context lines.

    Args:
        diff_content: Diff content.
        context_lines: Number of surrounding lines to include.

    Returns:
        Optimized diff content.
    """
    lines = diff_content.split("\n")
    result_lines = []

    # Track which lines are changed
    changed_line_indices = []
    for i, line in enumerate(lines):
        if line.startswith("+") or line.startswith("-"):
            changed_line_indices.append(i)

    # Include surrounding context for each changed line
    included_indices = set()
    for idx in changed_line_indices:
        start = max(0, idx - context_lines)
        end = min(len(lines), idx + context_lines + 1)

        for i in range(start, end):
            included_indices.add(i)

    # Add lines in order
    for i in sorted(included_indices):
        result_lines.append(lines[i])

    return "\n".join(result_lines)


def cost_optimized_changed_lines_into_batches(
    files: List[ReviewFile], max_prompt_payload_length: int
) -> List[List[PromptFile]]:
    """
    Batch changed lines using a cost-optimized method (including only changed lines and a few surrounding lines).

    Args:
        files: List of files.
        max_prompt_payload_length: Maximum prompt payload length.

    Returns:
        List of batched prompt files.
    """
    batches: List[List[PromptFile]] = []
    current_batch: List[PromptFile] = []
    current_batch_length = 0

    for file in files:
        # Extract changed lines with context if available
        if file["changedContent"]:
            optimized_content = extract_changed_lines_with_context(
                file["changedContent"], MAX_SURROUNDING_LINES
            )
        else:
            optimized_content = file["fileContent"]

        prompt_file = {"fileName": file["fileName"], "promptContent": optimized_content}

        file_length = get_length_of_file(prompt_file)

        # Start a new batch if adding this file would exceed the max length
        if current_batch_length + file_length > max_prompt_payload_length:
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_batch_length = 0

        current_batch.append(prompt_file)
        current_batch_length += file_length

    # Add the last batch
    if current_batch:
        batches.append(current_batch)

    return batches


def construct_test_case_generation_prompt(
    files: List[ReviewFile],
    test_files,
    max_prompt_length: int,
    review_type: str,
    review_language: str = "English",
    requirement: Optional[str] = None,
    to_judge_alignment=False,
    aligned_test_cases=None,
    unaligned_test_cases=None,
) -> List[str]:
    """
    Construct an array of prompts.

    Args:
        files: List of function code files.
        test_files: List of test files.
        max_prompt_length: Maximum prompt length.
        review_type: Review type (full, changed, or costOptimized).
        review_language: Review language.

    Returns:
        Array of prompts.
    """
    if to_judge_alignment:
        prompt_payloads = generate_prompt_payloads(
            files,
            review_type,
            TEST_CASE_GENERATION_PROMPT_PREFIX + TEST_CASE_GENERATION_PROMPT,
            max_prompt_length,
        )

        test_case_generation_prompt = TEST_CASE_GENERATION_PROMPT_PREFIX.replace(
            "{program_language}", get_language_name(files[0]["fileName"])
        ) + TEST_CASE_GENERATION_PROMPT.format(
            requirement=requirement,
            function_code=json.dumps(prompt_payloads),
            testcase=json.dumps(test_files),
            relevant_testcase="",
        )

        return [test_case_generation_prompt]
    else:
        function_codes = [
            {
                "fileName": file["fileName"],
                "fileContent": file["fileContent"],
                "changedContent": file["changedContent"],
            }
            for file in files
        ]
        test_case_generation_prompt = (
            ALIGNED_TEST_CASE_GENERATION_PROMPT.replace(
                "{program_language}", get_language_name(files[0]["fileName"])
            )
            .replace("{requirement}", requirement)
            .replace("{function_code}", json.dumps(function_codes))
            .replace("{testcase}", json.dumps(unaligned_test_cases))
            .replace("{aligned_testcases}", json.dumps(aligned_test_cases))
        )
        return [test_case_generation_prompt]


def generate_prompt_payloads(files, review_type, prompt_template, max_prompt_length):

    max_prompt_payload_length = max_prompt_length - len(prompt_template)
    prompt_payloads: List[List[PromptFile]] = []

    if review_type == "full":
        prompt_payloads = full_files_into_batches(files, max_prompt_payload_length)
    elif review_type == "changed":
        prompt_payloads = changed_lines_into_batches(files, max_prompt_payload_length)
    elif review_type == "costOptimized":
        prompt_payloads = cost_optimized_changed_lines_into_batches(
            files, max_prompt_payload_length
        )
    else:
        raise ValueError(
            f"Unsupported review type {review_type}. Please use one of: full, changed, costOptimized."
        )
    return prompt_payloads


def construct_requirement_generation_prompt(
    files: List[ReviewFile],
    max_prompt_length: int,
    review_type: str,
    review_language: str = "English",
) -> List[str]:
    """
    Construct an array of prompts.

    Args:
        files: List of files.
        max_prompt_length: Maximum prompt length.
        review_type: Review type (full, changed, or costOptimized).
        review_language: Review language.

    Returns:
        Array of prompts.
    """
    prompt_payloads = generate_prompt_payloads(
        files, review_type, REQUIREMENT_GENERATION_PROMPT, max_prompt_length
    )

    language_to_instruction_prompt = REQUIREMENT_GENERATION_PROMPT.replace(
        "{program_language}", get_language_name(files[0]["fileName"])
    ).replace("{review_language}", review_language)

    return [language_to_instruction_prompt + json.dumps(prompt_payloads)]
    # return [
    #     language_to_instruction_prompt + json.dumps(payload)
    #     for payload in prompt_payloads
    # ]


def construct_judge_alignment_prompt(
    requirement, function_files, test_cases, max_prompt_length
):
    """
    Construct an array of prompts to judge alignment between requirement and test cases.

    Args:
        requirement: Requirement.
        test_cases: Test cases.
        max_prompt_length: Maximum prompt length.

    Returns:
        Array of prompts.
    """
    batches = []
    current_batch = []
    current_batch_length = 0

    function_codes = [
        {
            "fileName": file["fileName"],
            "fileContent": file["fileContent"],
            "changedContent": file["changedContent"],
        }
        for file in function_files
    ]

    prompt = JUDGE_ALIGNMENT_PROMPT.replace(
        "{function_code}", json.dumps(function_codes)
    ).replace("{requirement}", requirement)
    for test_case in test_cases:
        test_case_length = len(test_case["code"])

        # Start a new batch if adding this file would exceed the max length
        if current_batch_length + test_case_length > max_prompt_length - len(prompt):
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_batch_length = 0

        current_batch.append(test_case)
        current_batch_length += test_case_length

    # Add the last batch
    if current_batch:
        batches.append(current_batch)

    return [prompt.replace("{testcase}", json.dumps(payload)) for payload in batches]


async def generate_requirement_msg(
    prompts, model_name, api_key, api_host, organization=None
):
    """
    Generate requirement message using an AI model.

    Args:
        prompts: Requirement prompt.
        model_name: Model name.
        api_key: API key.
        api_host: API host.
        organization: Organization ID (optional).

    Returns:
        Requirement message.
    """
    feedbacks = await ask_ai(prompts, model_name, api_key, api_host, organization)

    if len(feedbacks) > 0:
        return feedbacks[0]["requirement"]
    return ""


async def generate_test_cases(
    prompts, model_name, openai_api_key, openai_host, organization
):
    logger.debug(f"Prompts used:\n {prompts}")

    feedbacks = await ask_ai(
        prompts, model_name, openai_api_key, openai_host, organization
    )

    # Generate a markdown report
    markdown_report = genreate_test_case_report(feedbacks)

    logger.debug(f"Markdown report:\n{markdown_report}")
    logger.debug(f"Feedbacks:\n{feedbacks}")
    return markdown_report, feedbacks


async def get_aligned_test_cases(
    prompts, model_name, api_key, api_host, organization=None
):
    """
    Get aligned test cases.

    Args:
        prompts: List of prompts.
        model_name: Model name.
        api_key: API key.
        api_host: API host.
        organization: Organization ID (optional).

    Returns:
        Aligned test cases.
    """
    feedbacks = await ask_ai(prompts, model_name, api_key, api_host, organization)

    return feedbacks
