import os
import asyncio
from req_test_align.main import main
from dotenv import load_dotenv

load_dotenv(".env")


async def debug_github():
    # Simulate command line arguments, directly review and send to GitHub PR
    os.sys.argv = [
        "req-test-align",
        "generate",
        "--model",
        "gpt-4o-mini",
        "--reviewType",
        "changed",
        "--ci",
        "github",
        # "--commentPerFile",  # Optional, comment per file
        "--remote",
        f"{os.environ.get('GITHUB_REPOSITORY')}#{os.environ.get('GITHUB_PR_NUMBER')}",
        "--debug",
        "--testAffected",
    ]
    await main()


if __name__ == "__main__":
    asyncio.run(debug_github())
