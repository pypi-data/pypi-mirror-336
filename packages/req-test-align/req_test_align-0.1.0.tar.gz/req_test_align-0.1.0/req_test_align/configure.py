import os
import shutil
import subprocess
import getpass
from typing import Optional

from .utils.logger import logger
from .utils.utils import find_template_file


async def configure(setup_target: str = "github"):
    """
    Configure the tool.

    Args:
        setup_target: The platform to configure.
    """
    logger.info(f"Configuring {setup_target}...")

    # Create GitHub Actions workflow
    if setup_target == "github":
        await configure_github()
    # Local configuration
    elif setup_target == "local":
        await configure_local()
    else:
        logger.error(f"Unknown setup target: {setup_target}")
        return

    logger.info(f"{setup_target} configuration completed successfully.")


async def capture_api_host() -> Optional[str]:
    """
    Retrieve the user's OpenAI API key.

    Returns:
        API key
    """
    try:
        api_key = getpass.getpass("Please enter your OpenAI API host: ")
        return api_key if api_key else None
    except Exception as e:
        logger.error(f"Error retrieving API host: {str(e)}")
        return None


async def capture_api_key() -> Optional[str]:
    """
    Retrieve the user's OpenAI API key.

    Returns:
        API key
    """
    try:
        api_key = getpass.getpass("Please enter your OpenAI API key: ")
        return api_key if api_key else None
    except Exception as e:
        logger.error(f"Error retrieving API key: {str(e)}")
        return None


async def configure_github():
    """Configure GitHub."""
    try:
        github_workflow_template = find_template_file("github-pr.yml")

        workflows_dir = os.path.join(os.getcwd(), ".github", "workflows")
        os.makedirs(workflows_dir, exist_ok=True)

        workflow_file = os.path.join(workflows_dir, "req-align-test.yml")
        shutil.copyfile(github_workflow_template, workflow_file)

        logger.info(f"GitHub Actions workflow created: {workflow_file}")

        api_host = await capture_api_host()
        api_key = await capture_api_key()

        if not api_key:
            logger.error(
                "API key not provided. Please manually add the OPENAI_API_KEY secret to your GitHub repository."
            )
            return

        try:
            # Check if GitHub CLI is installed and authenticated
            subprocess.run("gh auth status || gh auth login", shell=True, check=True)

            # Set the secret
            subprocess.run(
                f"gh secret set OPENAI_API_KEY --body={api_key}", shell=True, check=True
            )

            logger.info(
                "Successfully added OPENAI_API_KEY secret to your GitHub repository."
            )

            subprocess.run(
                f"gh secret set OPEN_API_HOST --body={api_host}", shell=True, check=True
            )

            logger.info(
                "Successfully added OPEN_API_HOST secret to your GitHub repository."
            )

        except Exception as e:
            logger.error(
                "It seems that GitHub CLI is not installed or there was an error during authentication. "
                "Don't forget to manually add OPENAI_API_KEY to Repository Settings / Environment / Actions / Repository Secrets."
            )
            logger.debug(f"Error details: {str(e)}")
    except Exception as e:
        logger.error(f"Error configuring GitHub: {str(e)}")


async def configure_local():
    """Configure the local environment."""
    api_host = await capture_api_host()
    api_key = await capture_api_key()

    if not api_key:
        logger.error(
            "API key not provided. Please manually set the OPENAI_API_KEY environment variable."
        )
        return

    # Create .env file
    env_file = os.path.join(os.getcwd(), ".env")
    with open(env_file, "w") as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
        f.write(f"OPENAI_API_HOST={api_host}\n")

    logger.info(f".env file created: {env_file}")
    logger.info(
        "Make sure to load this environment variable before running code review."
    )
