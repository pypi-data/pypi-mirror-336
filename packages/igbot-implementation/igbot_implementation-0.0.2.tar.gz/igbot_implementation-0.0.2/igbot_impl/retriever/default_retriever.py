from langchain_core.retrievers import BaseRetriever

from igbot_base.igbot_base.retriever import Retriever


class DefaultRetriever(Retriever):

    def __init__(
            self,
            retriever: BaseRetriever):
        super().__init__()
        self.__retriever = retriever

    def get_relevant_data(self, query: str):
        contents = [doc.page_content for doc in self.__retriever.invoke(input=query)]
        return "\n".join(contents)
