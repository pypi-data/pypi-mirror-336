import asyncio
import os

from req_test_align.main import main
from req_test_align.utils.logger import logger
from dotenv import load_dotenv

load_dotenv(".env")

logger.set_debug(True)


async def debug():
    # 1. Normal test
    # os.sys.argv = [
    #     "req-test-align",
    #     "generate",
    #     "--model",
    #     "gpt-4o-mini",
    #     "--reviewType",
    #     "full",
    #     "--debug",
    #     "--requirement",
    #     "The code must implement a function to find the minimum value in a list of numbers.",
    # ]

    # 2. Test with pytest
    # os.sys.argv = [
    #     "req-test-align",
    #     "generate",
    #     "--model",
    #     "gpt-4o-mini",
    #     "--reviewType",
    #     "full",
    #     "--debug",
    #     "--testAffected",
    # ]
    # await main()

    # 2. Test with pytest
    os.sys.argv = [
        "req-test-align",
        "generate",
        "--model",
        "gpt-4o-mini",
        "--reviewType",
        "full",
        "--debug",
        "--testAffected",
        "--testTarget",
        "tests/test_discount.py",
        "tests",
    ]
    await main()


if __name__ == "__main__":
    asyncio.run(debug())
