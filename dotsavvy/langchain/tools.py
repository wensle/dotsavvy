from typing import Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool

from dotsavvy.services.vectorstore import create_pinecone_vectorstore
from dotsavvy.utils.env_variables import get_env_variable


class DOTFrameworkKnowledgeBase(BaseTool):
    name = "Search the DOT framework Knowledge base"
    description = (
        "Useful for when you need to answer knowledge questions about the DOT "
        "framework, provide tips on how to use the DOT Framework, or provide examples "
        "of how others have used the DOT Framework."
    )

    def _run(
        self,
        question: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        openai_api_key: str = get_env_variable("DOTSAVVY_OPENAI_API_KEY")
        llm_name: str = get_env_variable("DOTSAVVY_LLM_NAME")
        llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=llm_name)
        vectorstore = create_pinecone_vectorstore()
        qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )
        return qa_with_sources(question)

    async def _arun(
        self,
        question: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Search ictresearchmethods.nl")
