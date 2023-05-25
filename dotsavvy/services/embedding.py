from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings

from dotsavvy.utils.env_variables import get_env_variable


def embed_document(text: str, embedding_model_name: str | None = None) -> List[float]:
    embedding_model_name = embedding_model_name or get_env_variable(
        "DOTSAVVY_EMBEDDING_MODEL_NAME"
    )
    open_api_key: str = get_env_variable("OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=embedding_model_name, openai_api_key=open_api_key)
    res: List[List[float]] = embed.embed_documents([text])
    if len(res) != 1:
        raise ValueError(
            f"Expected exactly one embedding, got {len(res)}. Text: {text}, "
            f"embeddings: {res}"
        )
    return res[0]


def embed_documents(
    text: list[str], embedding_model_name: str | None = None
) -> List[List[float]]:
    embedding_model_name = embedding_model_name or get_env_variable(
        "DOTSAVVY_EMBEDDING_MODEL_NAME"
    )
    open_api_key: str = get_env_variable("OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=embedding_model_name, openai_api_key=open_api_key)
    res: List[List[float]] = embed.embed_documents(text)
    return res


def embed_query(text: str, embedding_model_name: str | None = None):
    embedding_model_name = embedding_model_name or get_env_variable(
        "DOTSAVVY_EMBEDDING_MODEL_NAME"
    )
    open_api_key: str = get_env_variable("OPENAI_API_KEY")
    embed = OpenAIEmbeddings(model=embedding_model_name, openai_api_key=open_api_key)
    res: List[float] = embed.embed_query(text)
    return res
