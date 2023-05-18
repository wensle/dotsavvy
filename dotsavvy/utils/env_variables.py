import os
from typing import Optional


def get_env_variable(key: str) -> str:
    """Get an environment variable.

    Args:
        key (str): The key of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not found.
    """
    value: Optional[str] = os.environ.get(key)
    if not value:
        raise ValueError(f"Environment variable {key} not found.")
    return value
