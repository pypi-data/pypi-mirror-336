# REQ-TEST-ALIGN

A tool to align requirements and test cases for your Python projects.

## Description

REQ-TEST-ALIGN analyzes your code changes and automatically generates or updates test cases to ensure they align with new requirements. It can be used locally or integrated into your GitHub workflows.

## Features

- Automatic test case generation based on code changes
- Integration with GitHub Actions
- Support for multiple programming languages
- Configurable review types
- Test generation focused on affected files

## Installation

You can install REQ-TEST-ALIGN using pip:

```
pip install req-test-align
```

or install it locally:

```
pip install -e .
```

## Configuration

Before using the tool, you need to configure it:

```
For GitHub integration

req-test-align configure --setupTarget github

# For local usage

req-test-align configure --setupTarget local 
```

The configuration process will prompt you for your OpenAI API key and host.

## Usage

### Basic Usage

To generate test cases for your project:

```
req-test-align generate
```

### Advanced Options

```
# Generate test cases for affected files only

req-test-align generate --testAffected

# Specify a model to use

req-test-align generate --model gpt-4o-mini

# Set the review type

req-test-align generate --reviewType [full|changed|costOptimized]

# Use a specific natural language for the output

req-test-align generate --review_language English

# Enable debug logging

req-test-align generate --debug

# Specify a requirement explicitly

req-test-align generate --requirement "The system must validate user input"

# Specify target files for testing

req-test-align generate --testTarget tests/test_module.py
```

### GitHub Integration

For GitHub Actions integration, add the following workflow file to your repository at req-test-align.yml:

```
name: Requirements Test Alignment

on:

  pull_request:

    types: [opened, synchronize]

jobs:

  align:

    runs-on: ubuntu-latest

    permissions:

      contents: read

      pull-requests: write

    steps:

      - uses: actions/checkout@v3

        with:

          fetch-depth: 0

      - name: Set up Python

        uses: actions/setup-python@v4

        with:

          python-version: '3.10'

      - name: Install dependencies

        run: |

          python -m pip install --upgrade pip

          pip install req-test-align

      - name: Run requirements test alignment

        env:

          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

          GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}

          GITHUB_PR_TITLE: ${{ github.event.pull_request.title }}

          GITHUB_PR_DESCRIPTION: ${{ github.event.pull_request.body }}

          GITHUB_REPOSITORY: ${{ github.repository }}

          GITHUB_BASE_REF: ${{ github.base_ref }}

        run: |

          req-test-align generate --ci github --model gpt-4o-mini --reviewType changed --debug --testAffected
```

## Requirements

- Python 3.7 or higher
- OpenAI API key
- GitHub token (for GitHub integration)