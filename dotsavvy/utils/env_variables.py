import os
from typing import Optional

from dotenv import load_dotenv


def get_env_variable(key: str) -> str:
    """Get an environment variable.

    Args:
        key (str): The key of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not found.
    """
    load_dotenv()
    value: Optional[str] = os.environ.get(key)
    if not value:
        raise ValueError(
            f"Environment variable {key} not found. Please set it using "
            f"`export {key}=<value>` in your terminal or set the variable in your "
            f".env file e.g. {key}=<value>."
        )
    return value
