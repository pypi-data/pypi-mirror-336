from langchain.retrievers import SelfQueryRetriever
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores import VectorStore

from igbot_base.igbot_base.retriever import Retriever


class SelfQuery(Retriever):

    def __init__(
            self,
            vectorstore: VectorStore,
            document_content_description: str,
            model: BaseLanguageModel,
            metadata_field_info):
        super().__init__()
        self.__retriever = SelfQueryRetriever.from_llm(model, vectorstore, document_content_description, metadata_field_info,
                                           enable_limit=False, use_original_query=True)

    def get_relevant_data(self, query: str):
        contents = [doc.page_content for doc in self.__retriever.invoke(input=query)]
        metadata = [doc.metadata for doc in self.__retriever.invoke(input=query)]
        return "\n".join(contents) + str(metadata)
