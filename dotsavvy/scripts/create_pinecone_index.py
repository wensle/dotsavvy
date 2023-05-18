import pinecone
from dotenv import load_dotenv

from dotsavvy.utils.env_variables import get_env_variable

# Constants
_DISTANCE_METRIC = "cosine"
"""OpenAI recommends cosine similarity for text embeddings, see
https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use
"""
_EMBEDDING_DIMENSION = 1536
"""OpenAI's text-embedding-ada-002 model has an embedding dimension of 1536, see
https://platform.openai.com/docs/guides/embeddings/second-generation-models"""

load_dotenv()


def create_index() -> None:
    api_key: str = get_env_variable("DOTSAVVY_PINECONE_API_KEY")
    environment: str = get_env_variable("DOTSAVVY_PINECONE_ENVIRONMENT")
    pinecone.init(api_key=api_key, environment=environment)
    index: str = get_env_variable("DOTSAVVY_PINECONE_INDEX")
    pinecone.create_index(
        name=index,
        dimension=_EMBEDDING_DIMENSION,
        metric=_DISTANCE_METRIC,
    )


if __name__ == "__main__":
    create_index()
