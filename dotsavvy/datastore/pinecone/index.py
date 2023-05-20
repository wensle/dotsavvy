import pinecone
from pinecone import GRPCIndex

from dotsavvy.utils.env_variables import get_env_variable


def init_pinecone() -> None:
    api_key: str = get_env_variable("DOTSAVVY_PINECONE_API_KEY")
    environment: str = get_env_variable("DOTSAVVY_PINECONE_ENVIRONMENT")
    pinecone.init(api_key=api_key, environment=environment)


def get_GRPC_index() -> GRPCIndex:
    init_pinecone()
    index_name: str = get_env_variable("DOTSAVVY_PINECONE_INDEX_NAME")
    return pinecone.GRPCIndex(index_name)
