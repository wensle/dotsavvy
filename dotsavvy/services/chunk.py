from typing import List, Optional
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)

# Constants
_CHUNK_SIZE = 100
_CHUNK_OVERLAP = 20
_ENCODING_NAME = "cl100k_base"
_MODEL_NAME = "gpt-3.5-turbo"


def get_text_chunks(
    text: str, chunk_size: Optional[int], chunk_overlap: Optional[int]
) -> List[str]:
    """
    Splits the provided text into smaller chunks using the
    RecursiveCharacterTextSplitter.

    The RecursiveCharacterTextSplitter divides text into chunks based on a list of
    characters, prioritizing splitting at paragraph breaks, then at line breaks, spaces,
    and if necessary, any character. This maintains continuity and semantic relationship
    as much as possible.


    """
    # Use the provided values or the default ones
    chunk_size = chunk_size or _CHUNK_SIZE
    chunk_overlap = chunk_overlap or _CHUNK_OVERLAP

    text_splitter: RecursiveCharacterTextSplitter = (
        RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            encoding_name=_ENCODING_NAME,
            model_name=_MODEL_NAME,
        )
    )
    chunks = text_splitter.split_text(text)
    return chunks
