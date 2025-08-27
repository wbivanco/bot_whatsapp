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
            model_name="gpt-4o-mini",
            temperature=0.3  # Temperatura más baja para respuestas más precisas
        )
        manager = EmbeddingsManager("openai", api_key, persist_directory)
        stored_embeddings = manager.get_embeddings()       
        QA_chain = llm_manager.initialice_retriever(
            llm, 
            stored_embeddings,
            search_type="similarity",
            num_result=3  # Aumentar el número de resultados para mejor cobertura
        )
        
        # Debug: ver qué documentos se recuperan (comentar en producción)
        # print(f"Pregunta del usuario: {user_message}")
        # retriever = stored_embeddings.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        # docs = retriever.get_relevant_documents(user_message)
        # print(f"Documentos recuperados: {len(docs)}")
        # for i, doc in enumerate(docs):
        #     print(f"Doc {i+1}: {doc.metadata.get('source', 'Sin fuente')}")
        #     print(f"Contenido: {doc.page_content[:200]}...")
        #     print("---")
        
        bot_response = llm_manager.get_response_retriever_without_memory(QA_chain, user_message) 

        return bot_response
    except Exception as e:
        print(f"Error: {e}")
