from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever

from igbot_base.igbot_base.retriever import Retriever


class Filter(Retriever):

    def __init__(
            self,
            retriever: BaseRetriever,
            model: BaseLanguageModel):
        super().__init__()
        compressor = LLMChainFilter.from_llm(model)
        self.__retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

    def get_relevant_data(self, query: str):
        contents = [doc.page_content for doc in self.__retriever.invoke(input=query)]
        return "\n".join(contents)
