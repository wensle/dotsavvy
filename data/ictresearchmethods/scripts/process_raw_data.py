"""Process raw data for ICT Research Methods Wiki to separate collections of texts and
metadata objects."""
import json
from pathlib import Path
from typing import Generator
from uuid import uuid4

from config import ICT_RESEARCH_METHODS_BASE_DIR

from dotsavvy.datastore.pinecone.types import METADATA


# Constants
_INPUT_DIR: Path = ICT_RESEARCH_METHODS_BASE_DIR / "raw_data"
_OUTPUT_DIR: Path = ICT_RESEARCH_METHODS_BASE_DIR / "processed_data"
_OUTPUT_FILE_PATH: Path = _OUTPUT_DIR / "processed_data.json"


def process_file(file: dict[str]) -> tuple[str, METADATA]:
    text: str = file["title"] + "\n\n" + file["content"]
    text = (
        text.replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("…", "...")
        .replace("—", "-")
        .replace("\n ", "\n")
    )
    metadata: METADATA = {
        "title": file["title"],
        "categories": file["categories"],
        "source": file["full_url"],
        "backlinks": file["backlinks"],
        "text": text,
        "document_id": str(uuid4()),
    }
    return text, metadata


def process_dir_generator(
    input_dir: Path,
) -> Generator[tuple[str, METADATA], None, None]:
    for raw_data_file in input_dir.glob("*.json"):
        with open(raw_data_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            processed_file = process_file(raw_data)
            yield processed_file


def main(
    input_dir: Path | None = None,
    output_dir: Path | None = None,
    output_file_path: Path | None = None,
) -> None:
    input_dir = input_dir or _INPUT_DIR
    if not input_dir.exists():
        raise FileNotFoundError(f"Path to the directory {input_dir} not found.")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory {input_dir} is not a directory.")
    texts, metadatas = zip(*process_dir_generator(input_dir))
    output_dir = output_dir or _OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file_path = output_file_path or _OUTPUT_FILE_PATH
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump({"texts": texts, "metadatas": metadatas}, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
