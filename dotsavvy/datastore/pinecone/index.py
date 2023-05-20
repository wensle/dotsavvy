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


def get_GRPC_index() -> GRPCIndex:
    init_pinecone()
    index_name: str = get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    return pinecone.GRPCIndex(index_name)


def get_REST_index() -> Index:
    init_pinecone()
    index_name: str = get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    return pinecone.Index(index_name)


def create_index() -> None:
    init_pinecone()
    index_name: str = get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    pinecone.create_index(
        name=index_name,
        dimension=_EMBEDDING_DIMENSION,
        metric=_DISTANCE_METRIC,
    )


def delete_index() -> None:
    init_pinecone()
    index_name: str = get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    pinecone.delete_index(name=index_name)
