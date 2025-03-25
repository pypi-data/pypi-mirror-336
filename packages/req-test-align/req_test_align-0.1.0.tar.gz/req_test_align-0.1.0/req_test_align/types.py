from enum import Enum
from typing import List, Optional, TypedDict


class PlatformOptions(str, Enum):
    GITHUB = "github"
    LOCAL = "local"


class ReviewArgs(TypedDict, total=False):
    command: str
    ci: Optional[str]
    setupTarget: str
    # commentPerFile: bool
    model: str
    reviewType: str
    review_language: Optional[str]
    remote: Optional[str]
    org: Optional[str]
    provider: str
    debug: bool
    requirement: Optional[str]
    testAffected: bool
    testTarget: List[str]


class ReviewFile(TypedDict):
    fileName: str
    fileContent: str
    changedContent: str


class PromptFile(TypedDict):
    fileName: str
    promptContent: str


class Review(TypedDict):
    reasoning: str


class TestCase(TypedDict):
    status: str
    testcase: str
    line: int
    reason: str


class TestFile(TypedDict):
    file: str
    testcases: List[TestCase]


class CreateFileCommentData(TypedDict):
    feedback: TestFile
    signOff: str
    owner: str
    repo: str
    pull_number: int
    commit_id: str
