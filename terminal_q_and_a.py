import openai
import yaml
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from typing import List, Tuple
from utils.load_config import LoadConfig

# For loading OpenAI credentials
APPCFG = LoadConfig()

with open("Directory") as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

# LLM config
llm_engine = app_config["llm_config"]["model"]
llm_system_role = app_config["llm_config"]["llm_system_role"]
llm_temperature = app_config["llm_config"]["temperature"]

# Retrieval config
k = app_config["retrieval_config"]["k"]

# Load the embedding function
embedding = OpenAIEmbeddings()
# Load the vector database
vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                  embedding_function=embedding)

print("Number of vectors in vectorDB:", vectordb._collection.count())

# Set your OpenAI API key
openai.api_key = "API KEY"

# Prepare the RAG with OpenAI in terminal
while True:
    question = input("\n\nEnter your question or press 'q' to exit: ")
    if question.lower() == 'q':
        break
    question = "# user new question:\n" + question
    docs = vectordb.similarity_search(question, k=APPCFG.k)
    retrieved_docs_page_content: List[Tuple] = [
        str(x.page_content)+"\n\n" for x in docs]
    retrived_docs_str = "# Retrieved content:\n\n" + str(retrieved_docs_page_content)
    prompt = retrived_docs_str + "\n\n" + question
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change model to engine
        messages=[
            {"role": "system", "content": APPCFG.llm_system_role},
            {"role": "user", "content": prompt}
        ]
    )
    print(response['choices'][0]['message']['content'])
