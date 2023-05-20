import os
from typing import Optional

from dotenv import load_dotenv

from config import DOT_ENV_FILE_PATH


def get_env_variable(key: str) -> str:
    """Get an environment variable.

    Args:
        key (str): The key of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not found.
    """
    result: bool = load_dotenv(DOT_ENV_FILE_PATH)
    if result is False:
        raise ValueError("Could not load .env file")
    value: Optional[str] = os.environ.get(key)
    if not value:
        raise ValueError(
            f"Environment variable {key} not found. Please set it using "
            f"`export {key}='your value'` in your terminal or set the variable in "
            f"your .env file e.g. {key}='your value'."
        )
    return value
