import pinecone
from pinecone import GRPCIndex, Index

from dotsavvy.utils.env_variables import get_env_variable

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
