import os
from pathlib import Path

# Get the project root directory
DOTSAVVY_ROOT_DIR = Path(
    os.environ.get("ROOT_DIR", os.path.dirname(os.path.abspath(__file__)))
)

# Define the data directory
DOTSAVVY_DATA_DIR = DOTSAVVY_ROOT_DIR / "data"
