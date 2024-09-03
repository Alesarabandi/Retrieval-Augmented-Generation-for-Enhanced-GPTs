
import openai
import os
from dotenv import load_dotenv
import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from pyprojroot import here
import shutil

load_dotenv()


class LoadConfig:
    """
   This class handles loading settings from a file called 'app_config.yml'. These settings include configurations for language models,
    data retrieval, summarizing text, and managing memory. Additionally, 
    the class sets up OpenAI API credentials and manages directories by creating or removing them as needed.

   
    """

    def __init__(self) -> None:
        with open(here("Direcotry")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # LLM configs
        self.llm_engine = app_config["llm_config"]["model"]
        self.llm_system_role = app_config["llm_config"]["llm_system_role"]
        self.persist_directory = str(here(
            app_config["directories"]["persist_directory"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.custom_persist_directory = str(here(
            app_config["directories"]["custom_persist_directory"]))
        self.embedding_model = OpenAIEmbeddings()

        # Retrieval configs
        self.data_directory = app_config["directories"]["data_directory"]
        self.k = app_config["retrieval_config"]["k"]
        self.embedding_model_engine = app_config["embedding_model_config"]["engine"]
        self.chunk_size = app_config["splitter_config"]["chunk_size"]
        self.chunk_overlap = app_config["splitter_config"]["chunk_overlap"]
        # Memory
        self.number_of_q_a_pairs = app_config["memory"]["number_of_q_a_pairs"]

        # Load OpenAI credentials
        self.load_openai_cfg()

        # clean up the upload doc vectordb if it exists
        self.create_directory(self.persist_directory)
        self.remove_directory(self.custom_persist_directory)

    def load_openai_cfg(self):
        """
        Load OpenAI configuration settings.

        This function sets the OpenAI API configuration settings which is the API type.

        """
        
        openai.api_key = os.getenv("API KEY")

    def create_directory(self, directory_path: str):
        """
        Create a directory if it does not exist.

        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def remove_directory(self, directory_path: str):
        """
        Removes the specified directory.

        """
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory_path}' does not exist.")