from langchain.vectorstores import Pinecone
from dotsavvy.datastore.pinecone.index import get_REST_index
from dotsavvy.services.embedding import embed_query


_TEXT_KEY = "text"


def create_pinecone_vectorstore(text_key: str | None = None) -> Pinecone:
    text_key = text_key or _TEXT_KEY
    index = get_REST_index()
    return Pinecone(
        index=index,
        embedding_function=embed_query,
        text_key=text_key,
    )
