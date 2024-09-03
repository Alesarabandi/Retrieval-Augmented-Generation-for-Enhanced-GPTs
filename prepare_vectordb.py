from langchain.vectorstores import Chroma
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings


class PrepareVectorDB:
    """
This class helps us create a special database called VectorDB using OpenAI embeddings.
 OpenAI embeddings are like unique fingerprints for words or sentences, capturing their meaning 
 and context. By using these embeddings, we can understand and work with text in a smart way.

The class is useful because it allows us to load documents, break them into smaller parts,
 and create a database with these parts and their embeddings. It also includes methods to prepare
 everything and save the VectorDB once it's ready. Essentially,
 this class makes it easier to work with documents and embeddings in our projects.
    """

    def __init__(
            self,
            data_directory: str,
            persist_directory: str,
            embedding_model_engine: str,
            chunk_size: int,
            chunk_overlap: int
    ) -> None:
        """
        Initialize the PrepareVectorDB instance.

        """

        self.embedding_model_engine = embedding_model_engine
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        self.data_directory = data_directory
        self.persist_directory = persist_directory
        self.embedding = OpenAIEmbeddings()

    def __load_all_documents(self) -> List:

        """

        Load all documents from the specified directory.

        """
        doc_counter = 0
        if isinstance(self.data_directory, list):
            print("Loading the uploaded documents...")
            docs = []
            for doc_dir in self.data_directory:
                docs.extend(PyMuPDFLoader(doc_dir).load())
                doc_counter += 1
            print("Number of loaded documents:", doc_counter)
            print("Number of pages:", len(docs), "\n\n")
        else:
            print("Loading documents manually...")
            document_list = os.listdir(self.data_directory)
            docs = []
            for doc_name in document_list:
                docs.extend(PyMuPDFLoader(os.path.join(
                    self.data_directory, doc_name)).load())
                doc_counter += 1
            print("Number of loaded documents:", doc_counter)
            print("Number of pages:", len(docs), "\n\n")

        return docs

    def __chunk_documents(self, docs: List) -> List:
        """
        Chunk the loaded documents using the specified text splitter.

        """
        print("Chunking documents...")
        chunked_documents = self.text_splitter.split_documents(docs)
        print("Number of chunks:", len(chunked_documents), "\n\n")
        return chunked_documents

    def prepare_and_save_vectordb(self):
        """
        Load, chunk, and create a VectorDB with OpenAI embeddings, and save it.
        """
        docs = self.__load_all_documents()
        chunked_documents = self.__chunk_documents(docs)
        print("Preparing vectordb...")
        vectordb = Chroma.from_documents(
            documents=chunked_documents,
            embedding=self.embedding,
            persist_directory=self.persist_directory
        )
        print("VectorDB is created and saved.")
        print("Number of vectors in vectorDB:",
              vectordb._collection.count(), "\n\n")
        return vectordb
