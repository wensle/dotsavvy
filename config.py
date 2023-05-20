import os
from pathlib import Path

DOTSAVVY_ROOT_DIR = Path(
    os.environ.get("ROOT_DIR", os.path.dirname(os.path.abspath(__file__)))
)
"""The root directory of the dotsavvy package."""

DOTSAVVY_DATA_DIR: Path = DOTSAVVY_ROOT_DIR / "data"
"""The directory for the data used by the dotsavvy package.""" ""

ICT_RESEARCH_METHODS_BASE_DIR: Path = DOTSAVVY_DATA_DIR / "ictresearchmethods"
"""The base directory for the ICT Research Methods data, also including scripts and
notebooks."""
