from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings

from dotsavvy.utils.env_variables import get_env_variable

# Constants
_MODEL_NAME = "text-embedding-ada-002"


def embed_document(text: str) -> List[List[float]]:
    open_api_key: str = get_env_variable("DOTSAVVY_OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=_MODEL_NAME, openai_api_key=open_api_key)
    res: List[List[float]] = embed.embed_documents([text])
    if len(res) != 1:
        raise ValueError(
            f"Expected exactly one embedding, got more. Text: {text}, embeddings: {res}"
        )
    return res[0]


def embed_query(text: str):
    open_api_key: str = get_env_variable("DOTSAVVY_OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=_MODEL_NAME, openai_api_key=open_api_key)
    res: List[float] = embed.embed_query(text)
    return res
