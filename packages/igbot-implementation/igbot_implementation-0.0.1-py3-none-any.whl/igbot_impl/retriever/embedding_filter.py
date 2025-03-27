from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_core.retrievers import BaseRetriever

from igbot_base.igbot_base.retriever import Retriever


class EmbeddingFilter(Retriever):

    def __init__(
            self,
            retriever: BaseRetriever,
            embedding_function,
            similarity_threshold):
        super().__init__()

        embeddings_filter = EmbeddingsFilter(embeddings=embedding_function, similarity_threshold=similarity_threshold)
        self.__retriever = ContextualCompressionRetriever(base_compressor=embeddings_filter,
                                                          base_retriever=retriever)

    def get_relevant_data(self, query: str):
        contents = [doc.page_content for doc in self.__retriever.invoke(input=query)]
        return "\n".join(contents)
