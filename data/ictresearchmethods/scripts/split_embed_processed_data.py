import json
import pickle
from pathlib import Path
from uuid import uuid4

from config import ICT_RESEARCH_METHODS_BASE_DIR
from dotsavvy.datastore.pinecone.types import METADATA
from dotsavvy.services.chunk import create_recursive_tiktoken_splitter
from dotsavvy.services.embedding import embed_documents

_INPUT_FILE_PATH: Path = (
    ICT_RESEARCH_METHODS_BASE_DIR / "processed_data" / "processed_data.json"
)
_OUTPUT_FILE_PATH: Path = (
    ICT_RESEARCH_METHODS_BASE_DIR / "processed_data" / "embedding_tuples.pkl"
)


def ingest_file(filepath: str | Path) -> tuple[list[str], list[METADATA]]:
    """A helper function to load the input file containing processed data."""
    with open(filepath, "r") as f:
        json_obj = json.load(f)
    return json_obj["texts"], json_obj["metadatas"]


def main(
    input_file_path: str | Path | None = None,
    output_file_path: str | Path | None = None,
) -> None:
    input_file_path = input_file_path or _INPUT_FILE_PATH
    output_file_path = output_file_path or _OUTPUT_FILE_PATH

    texts, metadatas = ingest_file(input_file_path)

    text_splitter = create_recursive_tiktoken_splitter()
    documents = text_splitter.create_documents(texts, metadatas)
    chunks = []
    metadatas = []
    uuids = []
    for doc in documents:
        chunks.append(doc.page_content)
        metadatas.append(doc.metadata)
        uuids.append(str(uuid4()))
    embeddings = embed_documents(chunks)
    embedding_tuples = list(zip(uuids, embeddings, metadatas))

    with open(_OUTPUT_FILE_PATH, "wb") as pkl:
        pickle.dump(embedding_tuples, pkl)


if __name__ == "__main__":
    main()
