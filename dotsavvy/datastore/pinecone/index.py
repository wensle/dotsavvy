import pinecone
from pinecone import GRPCIndex, Index

from dotsavvy.utils.env_variables import get_env_variable

# Constants
_DISTANCE_METRIC = "cosine"
"""OpenAI recommends cosine similarity for text embeddings, see
https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use
"""
_EMBEDDING_DIMENSION = 1536
"""OpenAI's text-embedding-ada-002 model has an embedding dimension of 1536, see
https://platform.openai.com/docs/guides/embeddings/second-generation-models"""
_METADATA_CONFIG: dict[str, list[str]] = {"indexed": ["categories", "backlinks"]}

# Global flag to indicate whether Pinecone has been initialized
_pinecone_initialized = False


def init_pinecone() -> None:
    global _pinecone_initialized
    if _pinecone_initialized:
        return
    api_key: str = get_env_variable("DOTSAVVY_PINECONE_API_KEY")
    environment: str = get_env_variable("DOTSAVVY_PINECONE_ENVIRONMENT")
    pinecone.init(api_key=api_key, environment=environment)
    _pinecone_initialized = True


def get_GRPC_index(index_name: str | None = None) -> GRPCIndex:
    index_name = index_name or get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    init_pinecone()
    return pinecone.GRPCIndex(index_name)


def get_REST_index(index_name: str | None = None) -> Index:
    index_name = index_name or get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    init_pinecone()
    return pinecone.Index(index_name)


def create_index(index_name: str | None = None) -> None:
    index_name = index_name or get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    init_pinecone()
    pinecone.create_index(
        name=index_name,
        dimension=_EMBEDDING_DIMENSION,
        metric=_DISTANCE_METRIC,
        metadata_config=_METADATA_CONFIG,
    )


def delete_index(index_name: str | None = None) -> None:
    index_name = index_name or get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    init_pinecone()
    pinecone.delete_index(name=index_name)
