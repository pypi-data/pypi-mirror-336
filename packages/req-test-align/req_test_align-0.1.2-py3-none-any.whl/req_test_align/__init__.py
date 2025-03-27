"""
REQ-TEST-ALIGN

A tool to align requirements and test cases for your Python projects.
"""

__version__ = "0.1.0"

# Export main functions for module usage
from .main import main, main_entry, get_changed_files
from .core.align_test_case import generate_aligned_test_cases
from .configure import configure

# Export key types for type annotations
from .types import (
    PlatformOptions,
    ReviewArgs,
    ReviewFile, 
    PromptFile,
    Review,
    TestCase,
    TestFile,
    CreateFileCommentData
)

# Define what symbols are exported when using "from req_test_align import *"
__all__ = [
    "main",
    "main_entry",
    "get_changed_files",
    "generate_aligned_test_cases",
    "configure",
    "PlatformOptions",
    "ReviewArgs",
    "ReviewFile",
    "PromptFile",
    "Review",
    "TestCase",
    "TestFile",
    "CreateFileCommentData"
]