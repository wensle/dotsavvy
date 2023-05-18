from typing import List, Optional
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Constants
_MODEL_NAME = "text-embedding-ada-002"

load_dotenv()


def get_embeddings(texts: List[str]) -> List[List[float]]:
    open_api_key: Optional[str] = os.environ.get("DOTSAVVY_OPENAI_API_KEY")
    if not open_api_key:
        raise ValueError(
            "OpenAI API key (DOTSAVVY_OPENAI_API_KEY) not found in environment "
            "variables."
        )
    embed = OpenAIEmbeddings(model=_MODEL_NAME, openai_api_key=open_api_key)
    res: List[List[float]] = embed.embed_documents(texts)
    return res
