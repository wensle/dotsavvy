import itertools
import json
from pathlib import Path
from typing import Generator, Iterable, Iterator
from uuid import uuid4

from config import ICT_RESEARCH_METHODS_BASE_DIR
from dotsavvy.datastore.pinecone.index import get_GRPC_index
from dotsavvy.datastore.pinecone.types import METADATA
from dotsavvy.services.chunk import create_recursive_tiktoken_splitter
from dotsavvy.services.embedding import embed_document

_UPSERT_BATCH_SIZE = 100
_INPUT_FILE_PATH: Path = (
    ICT_RESEARCH_METHODS_BASE_DIR / "processed_data" / "processed_data.json"
)


def upsert_batch_generator(
    vectors: Iterable, batch_size=int | None
) -> Generator[tuple, None, None]:
    """A helper function to break an iterable into chunks of size batch_size."""
    batch_size = batch_size or _UPSERT_BATCH_SIZE
    it: Iterator = iter(vectors)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def ingest_file(filepath: str | Path) -> tuple[list[str], list[METADATA]]:
    """A helper function to load the input file containing processed data."""
    with open(filepath, "r") as f:
        json_obj = json.load(f)
    return json_obj["texts"], json_obj["metadatas"]


def main(
    input_file_path: str | Path | None = None, upsert_batch_size: int | None = None
) -> None:
    input_file_path = input_file_path or _INPUT_FILE_PATH
    upsert_batch_size = upsert_batch_size or _UPSERT_BATCH_SIZE

    texts, metadatas = ingest_file(input_file_path)

    text_splitter = create_recursive_tiktoken_splitter()
    documents = text_splitter.create_documents(texts, metadatas)
    vector_tuples = [
        (str(uuid4()), embed_document(doc.page_content), doc.metadata)
        for doc in documents
    ]

    index = get_GRPC_index()

    index.upsert(vector_tuples, batch_size=upsert_batch_size)


if __name__ == "__main__":
    main()
