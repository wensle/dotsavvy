from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings

from dotsavvy.utils.env_variables import get_env_variable

# Constants
_MODEL_NAME = "text-embedding-ada-002"


def embed_documents(texts: List[str]) -> List[List[float]]:
    open_api_key: str = get_env_variable("DOTSAVVY_OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=_MODEL_NAME, openai_api_key=open_api_key)
    res: List[List[float]] = embed.embed_documents(texts)
    return res
