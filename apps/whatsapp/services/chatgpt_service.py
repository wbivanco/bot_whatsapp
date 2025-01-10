import os

from ia.llm.manage_llm import LlmManager
from ia.embeddings.manage_embeddings import EmbeddingsManager

from base.load_env import load_env

load_env()
api_key = os.getenv("OPENAI_API_KEY")
persist_directory = os.getenv("PERSIST_CHROMADB_FOLDER")

def get_bot_response(user_message):
    """ Obtiene la respuesta del bot (utilizando su base de conocimiento) a partir del mensaje del usuario. """
    try:
        llm_manager = LlmManager("openai")
        llm = llm_manager.initialice_llm_model(
            api_key=api_key, 
            model_name="gpt-4o-mini"
        )
        manager = EmbeddingsManager("openai", api_key, persist_directory)
        stored_embeddings = manager.get_embeddings()       
        QA_chain = llm_manager.initialice_retriever(llm, stored_embeddings)
        bot_response = llm_manager.get_response_retriever_without_memory(QA_chain, user_message) 

        return bot_response
    except Exception as e:
        print(f"Error: {e}")
