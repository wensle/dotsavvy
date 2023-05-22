from pathlib import Path
import pickle

from config import ICT_RESEARCH_METHODS_BASE_DIR, PDFS_BASE_DIR
from dotsavvy.datastore.pinecone.index import get_GRPC_index

_UPSERT_BATCH_SIZE = 100
_INPUT_FILE_PATH: Path = PDFS_BASE_DIR / "processed_data" / "embedding_tuples.pkl"


def main(
    input_file_path: str | Path | None = None, upsert_batch_size: int | None = None
) -> None:
    input_file_path = input_file_path or _INPUT_FILE_PATH
    upsert_batch_size = upsert_batch_size or _UPSERT_BATCH_SIZE

    with open(_INPUT_FILE_PATH, "rb") as pkl:
        embedding_tuples = pickle.load(pkl)

    index = get_GRPC_index()
    index.upsert(embedding_tuples, batch_size=upsert_batch_size)


if __name__ == "__main__":
    main()
