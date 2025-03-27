import os
import sys

from igbot_base.igbot_base.vectorstore import Vectorstore, Metadata
from igbot_impl.igbot_impl.retriever import DefaultRetriever

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


class ChromaVectorstore(Vectorstore):

    def __init__(self, db_name: str, embedding_function: Embeddings):
        self.__db_name = db_name
        self.__db = Chroma(persist_directory=db_name, embedding_function=embedding_function)
        self.__metadata = Metadata()
        self.__load_metadata()

    def get_db(self):
        return self.__db

    def remove_db(self):
        if os.path.exists(self.__db_name):
            self.__db.delete_collection()

    def get_dimensions_number(self):
        collection = self.__db._collection
        sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
        dimensions = len(sample_embedding)
        return dimensions

    def get_retriever(self, load_number_of_chunks):
        return DefaultRetriever(self.get_legacy_retriever(load_number_of_chunks))

    # TODO: needed?
    def get_legacy_retriever(self, load_number_of_chunks):
        return self.__db.as_retriever(search_kwargs={"k": load_number_of_chunks})

    def append(self, chunks):
        for documents in batch(chunks, 20):
            self.__db.add_documents(documents=documents)

        for chunk in chunks:
            for key in chunk.metadata.keys():
                self.__metadata.append(key, chunk.metadata[key])

        print(f"Vectorstore appended with {len(chunks)} documents")

    def get_metadata(self):
        return self.__metadata.get()

    def __load_metadata(self):
        collection = self.__db._collection
        result = collection.get(include=['metadatas'])
        metadatas = result['metadatas']
        for metadata in metadatas:
            for key in metadata.keys():
                self.__metadata.append(key, metadata[key])



