
import os
from utils.prepare_vectordb import PrepareVectorDB
from utils.load_config import LoadConfig
CONFIG = LoadConfig()


def upload_data_manually() -> None:
    """
   This function manually uploads data to the VectorDB.

It starts by creating a PrepareVectorDB instance with settings like data directory,
 where to save the database, the embedding model engine, chunk size, and chunk overlap. 
 Then, it checks if the VectorDB already exists in the specified save location. 
 If the VectorDB doesn't exist, it creates and saves it using the prepare_and_save_vectordb method. 
 If the VectorDB already exists, it simply prints a message indicating that.

    """
    prepare_vectordb_instance = PrepareVectorDB(
        data_directory=CONFIG.data_directory,
        persist_directory=CONFIG.persist_directory,
        embedding_model_engine=CONFIG.embedding_model_engine,
        chunk_size=CONFIG.chunk_size,
        chunk_overlap=CONFIG.chunk_overlap,
    )
    if not len(os.listdir(CONFIG.persist_directory)) != 0:
        prepare_vectordb_instance.prepare_and_save_vectordb()
    else:
        print(f"VectorDB already exists in {CONFIG.persist_directory}")
    return None


if __name__ == "__main__":
    upload_data_manually()
