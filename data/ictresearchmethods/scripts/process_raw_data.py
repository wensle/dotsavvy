"""Process raw data for ICT Research Methods Wiki to upsert into Pinecone."""
import json
from pathlib import Path

from config import ICT_RESEARCH_METHODS_BASE_DIR

from dotsavvy.datastore.pinecone.types import METADATA


# Constants
_INPUT_DATA_DIR: Path = ICT_RESEARCH_METHODS_BASE_DIR / "raw_data"
_OUTPUT_DATA_DIR: Path = ICT_RESEARCH_METHODS_BASE_DIR / "processed_data"


def create_processed_data_dir() -> None:
    if not _OUTPUT_DATA_DIR.exists():
        _OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)


def process_raw_data_file(raw_data: dict[str]) -> dict[str, str | METADATA]:
    text: str = raw_data["title"] + "\n\n" + raw_data["content"]
    metadata: METADATA = {
        "title": raw_data["title"],
        "categories": raw_data["categories"],
        "url": raw_data["full_url"],
        "backlinks": raw_data["backlinks"],
    }
    return {"text": text, "metadata": metadata}


def run() -> None:
    create_processed_data_dir()
    output_data_file: Path = _OUTPUT_DATA_DIR / "processed_data.json"
    output_data = []
    for raw_data_file in _INPUT_DATA_DIR.glob("*.json"):
        with open(raw_data_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        processed_data = process_raw_data_file(raw_data)
        output_data.append(processed_data)
    with open(output_data_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)


if __name__ == "__main__":
    run()
