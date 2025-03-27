import os
import re
import base64
import requests
from typing import Dict, List, Optional, Any, TypedDict

from ..types import ReviewFile, CreateFileCommentData, TestFile
from ..utils.logger import logger
from ..config import github_token
from ..config import SUPPORTED_FILES, EXCLUDED_KEYWORDS
from ..utils.commit_utils import (
    parse_patch_content,
    extract_changed_components,
    do_patch,
)
from ..utils.utils import generate_general_markdown_report


class OctokitRepoDetails(TypedDict):
    octokit: Any  # Use requests instead of octokit in Python
    owner: str
    repo: str
    pull_number: int


def get_octokit_repo_details() -> Optional[OctokitRepoDetails]:
    """
    Get GitHub repository details, including the octokit-like client, owner, repository name, and PR number.
    """
    github_token_value = github_token()
    github_repository = os.environ.get("GITHUB_REPOSITORY")
    github_pr_number_str = os.environ.get("GITHUB_PR_NUMBER")

    if not github_token_value or not github_repository or not github_pr_number_str:
        return None

    try:
        # Parse repository information
        owner, repo = github_repository.split("/")
        pull_number = int(github_pr_number_str)

        # Create a session-like object similar to octokit
        class GitHubClient:
            def __init__(self, token: str):
                self.token = token
                self.base_url = "https://api.github.com"
                self.session = requests.Session()
                self.session.headers.update(
                    {
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/vnd.github+json",
                    }
                )

            def get(
                self, endpoint: str, params: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                response = self.session.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()

            def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
                response = self.session.post(f"{self.base_url}{endpoint}", json=data)
                response.raise_for_status()
                return response.json()

            def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
                response = self.session.patch(f"{self.base_url}{endpoint}", json=data)
                response.raise_for_status()
                return response.json()

        octokit = GitHubClient(github_token_value)

        return {
            "octokit": octokit,
            "owner": owner,
            "repo": repo,
            "pull_number": pull_number,
        }
    except Exception as e:
        logger.error(f"Error getting octokit repository details: {str(e)}")
        return None


async def comment_on_file(octokit: Any, data: CreateFileCommentData) -> None:
    """
    Post a comment on a file.
    """
    feedback = data["feedback"]
    sign_off = data["signOff"]
    owner = data["owner"]
    repo = data["repo"]
    pull_number = data["pull_number"]
    commit_id = data["commit_id"]

    # Remove the first ./ from the file path
    feedback["file"] = feedback["file"].lstrip("./")
    # Build the comment content
    total_comment = generate_general_markdown_report(feedback)

    # Append the sign-off
    total_comment += sign_off

    try:
        # Retrieve existing comments on the file
        comments = octokit.get(f"/repos/{owner}/{repo}/pulls/{pull_number}/comments")

        added_functions = []
        for testcase in feedback["testcases"]:
            if testcase.get("added_functions"):
                added_functions.append(testcase)

            current_comment = generate_general_markdown_report(testcase)
            current_comment += sign_off
            do_comment(
                octokit,
                comments,
                feedback["file"],
                testcase["line"],
                owner,
                repo,
                pull_number,
                commit_id,
                current_comment,
                sign_off,
                start_line=testcase.get("startLine"),
            )

        if added_functions:
            current_comment = generate_general_markdown_report(
                {
                    "testcases": added_functions,
                }
            )
            do_comment(
                octokit,
                comments,
                feedback["file"],
                1,  # add to the first line
                owner,
                repo,
                pull_number,
                commit_id,
                current_comment,
                sign_off,
            )

    except Exception as e:
        logger.error(f"Error commenting on file: {str(e)}")


def do_comment(
    octokit,
    comments,
    file,
    line,
    owner,
    repo,
    pull_number,
    commit_id,
    current_comment,
    sign_off,
    start_line=None,
):
    # Check if a comment with the same sign-off already exists
    existing_comment_id = None
    for comment in comments:
        if (
            comment.get("body", "").endswith(sign_off)
            and file in comment.get("path", "")
            and line == comment.get("position", 0)
        ):
            existing_comment_id = comment["id"]
            break

    if existing_comment_id:
        # Update the existing comment
        octokit.patch(
            f"/repos/{owner}/{repo}/pulls/comments/{existing_comment_id}",
            {"body": current_comment},
        )
    else:
        # Create a new comment
        octokit.post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/comments",
            {
                "body": current_comment,
                "commit_id": commit_id,
                "path": file,
                "start_line": start_line or line,
                "line": line,
            },
        )


async def comment_per_file(feedbacks: List[TestFile], sign_off: str) -> None:
    """
    Post comments per file on the PR. If the bot has already commented on a file
    (i.e., a comment with the same sign-off exists), update the comment rather than creating a new one.
    The comment will be signed with the provided sign-off.

    Args:
        feedbacks: JSON feedback from the AI model.
        sign_off: The sign-off to use. This is also used as a key to check if the bot has already commented,
                  to update the comment if necessary rather than posting a new one.
    """
    octokit_repo_details = get_octokit_repo_details()
    if octokit_repo_details:
        octokit = octokit_repo_details["octokit"]
        owner = octokit_repo_details["owner"]
        repo = octokit_repo_details["repo"]
        pull_number = octokit_repo_details["pull_number"]

        # Get the PR and commit ID
        pull_request = octokit.get(f"/repos/{owner}/{repo}/pulls/{pull_number}")
        commit_id = pull_request["head"]["sha"]

        # Post feedback comment for each file
        for feedback in feedbacks:
            await comment_on_file(
                octokit,
                {
                    "feedback": feedback,
                    "signOff": sign_off,
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pull_number,
                    "commit_id": commit_id,
                },
            )


async def comment_on_pr(markdown_report: str, sign_off: str) -> None:
    """
    Post a comment on the PR. If the bot has already commented (i.e., a comment with the same sign-off exists),
    update the comment rather than creating a new one.
    The comment will be signed with the provided sign-off.

    Args:
        markdown_report: The report in Markdown format to post.
        sign_off: The sign-off to use. This is also used as a key to check if the bot has already commented,
                  to update the comment if necessary rather than posting a new one.
    """
    octokit_repo_details = get_octokit_repo_details()
    if octokit_repo_details:
        octokit = octokit_repo_details["octokit"]
        owner = octokit_repo_details["owner"]
        repo = octokit_repo_details["repo"]
        pull_number = octokit_repo_details["pull_number"]

        # Build the comment content
        comment_body = f"{markdown_report}\n\n{sign_off}"

        try:
            # Retrieve existing comments on the PR
            comments = octokit.get(
                f"/repos/{owner}/{repo}/issues/{pull_number}/comments"
            )

            # Check if a comment with the same sign-off already exists
            existing_comment_id = None
            for comment in comments:
                if comment.get("body", "").endswith(sign_off):
                    existing_comment_id = comment["id"]
                    break

            if existing_comment_id:
                # Update the existing comment
                octokit.patch(
                    f"/repos/{owner}/{repo}/issues/comments/{existing_comment_id}",
                    {"body": comment_body},
                )
            else:
                # Create a new comment
                octokit.post(
                    f"/repos/{owner}/{repo}/issues/{pull_number}/comments",
                    {"body": comment_body},
                )
        except Exception as e:
            logger.error(f"Error commenting on PR: {str(e)}")


def extract_pull_request_identifier(remote_pull_request: str) -> Dict[str, Any]:
    """
    Extract the owner, repository, and PR number from a remote pull request URL or identifier.

    Args:
        remote_pull_request: Remote pull request URL or identifier

    Returns:
        A dictionary containing the owner, repository, and PR number.
    """
    # Try matching the GitHub URL format
    url_pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    url_match = re.match(url_pattern, remote_pull_request)

    if url_match:
        owner, repo, pr_number = url_match.groups()
        return {"owner": owner, "repo": repo, "prNumber": int(pr_number)}

    # Try matching the short format: owner/repo#pr_number
    short_pattern = r"([^/]+)/([^#]+)#(\d+)"
    short_match = re.match(short_pattern, remote_pull_request)

    if short_match:
        owner, repo, pr_number = short_match.groups()
        return {"owner": owner, "repo": repo, "prNumber": int(pr_number)}

    raise ValueError(f"Invalid pull request identifier: {remote_pull_request}")


def is_eligible_for_review(filename: str, status: str) -> bool:
    """
    Check if the file meets the review eligibility criteria.

    Args:
        filename: File name
        status: File status

    Returns:
        True if the file is eligible for review; otherwise, False.
    """

    # Check if the file was removed
    if status == "removed":
        return False

    # Check the file extension
    _, extension = os.path.splitext(filename)
    if extension not in SUPPORTED_FILES:
        return False

    # Check if the filename contains excluded keywords
    for keyword in EXCLUDED_KEYWORDS:
        if keyword in filename.lower():
            return False

    return True


async def get_remote_pull_request_files(remote_pull_request: str) -> List[ReviewFile]:
    """
    Get files from a remote pull request.

    Args:
        remote_pull_request: Remote pull request URL or identifier

    Returns:
        List of review files.
    """
    pull_request_identifier = extract_pull_request_identifier(remote_pull_request)
    token_value = github_token()

    if not token_value:
        raise ValueError(
            "GitHub token is not set. Please set the GITHUB_TOKEN environment variable."
        )

    owner = pull_request_identifier["owner"]
    repo = pull_request_identifier["repo"]
    pr_number = pull_request_identifier["prNumber"]

    # Create GitHub client
    headers = {
        "Authorization": f"token {token_value}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        # Get PR files
        files_url = (
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
        )
        response = requests.get(files_url, headers=headers)
        response.raise_for_status()

        diff_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
        diff_headers = {
            "Authorization": f"token {token_value}",
            "Accept": "application/vnd.github.diff",
        }
        diff_response = requests.get(diff_url, headers=diff_headers)
        diff_content = diff_response.text
        raw_files = response.json()
        review_files = []

        for raw_file in raw_files:
            if not is_eligible_for_review(raw_file["filename"], raw_file["status"]):
                continue

            # Get file content
            contents_url = raw_file["contents_url"]
            content_response = requests.get(contents_url, headers=headers)
            content_response.raise_for_status()
            content_data = content_response.json()

            if "content" in content_data:
                file_content = base64.b64decode(content_data["content"]).decode("utf-8")

                parsed_changes = parse_patch_content(
                    raw_file["filename"], raw_file.get("patch", "").splitlines()
                )

                functions_before, test_cases_before = extract_changed_components(
                    content_data["path"],
                    file_content,
                    parsed_changes,
                    to_get_bugs=True,
                    language="python",
                    function_only=True,
                )

                patched_file_content = do_patch(
                    file_content,
                    diff_content,
                    file_path=content_data["path"],
                    reverse=True,
                )
                functions_after, test_cases_after = extract_changed_components(
                    content_data["path"],
                    patched_file_content,
                    parsed_changes,
                    to_get_bugs=False,
                    language="python",
                    function_only=True,
                )

                review_files.append(
                    {
                        "fileName": raw_file["filename"],
                        "fileContent": file_content,
                        "changedContent": raw_file.get("patch", ""),
                        "parsedChanges": parsed_changes,
                        "functions_after": functions_after,
                        "functions_before": functions_before,
                        "testCases_after": test_cases_after,
                        "testCases_before": test_cases_before,
                    }
                )

        return review_files
    except Exception as e:
        raise Exception(f"Failed to get remote pull request files: {str(e)}")
