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
        print(f"[ChatGPT Service] Procesando consulta: {user_message}")
        
        llm_manager = LlmManager("openai")
        llm = llm_manager.initialice_llm_model(
            api_key=api_key, 
            model_name="gpt-4o-mini",
            temperature=0.3  # Temperatura más baja para respuestas más precisas
        )
        
        if llm is None:
            print("[ChatGPT Service] Error: No se pudo inicializar el modelo LLM")
            return "error"
        
        print("[ChatGPT Service] Modelo LLM inicializado correctamente")
        
        manager = EmbeddingsManager("openai", api_key, persist_directory)
        stored_embeddings = manager.get_embeddings()
        
        if stored_embeddings is None:
            print("[ChatGPT Service] Error: No se pudieron cargar los embeddings")
            return "error"
        
        print("[ChatGPT Service] Embeddings cargados correctamente")
        
        QA_chain = llm_manager.initialice_retriever(
            llm, 
            stored_embeddings,
            search_type="similarity",
            num_result=3  # Aumentar el número de resultados para mejor cobertura
        )
        
        if QA_chain is None:
            print("[ChatGPT Service] Error: No se pudo inicializar el QA_chain")
            return "error"
        
        print("[ChatGPT Service] QA_chain inicializado, obteniendo respuesta...")
        
        # Debug: ver qué documentos se recuperan
        print(f"[ChatGPT Service] Consulta del usuario: {user_message}")
        retriever = stored_embeddings.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(user_message)
        print(f"[ChatGPT Service] Documentos recuperados: {len(docs)}")
        for i, doc in enumerate(docs):
            print(f"[ChatGPT Service] Doc {i+1}: {doc.metadata.get('source', 'Sin fuente')}")
            print(f"[ChatGPT Service] Contenido: {doc.page_content[:200]}...")
        
        bot_response = llm_manager.get_response_retriever_without_memory(QA_chain, user_message)
        
        if bot_response is None or bot_response == "":
            print("[ChatGPT Service] Error: La respuesta del bot está vacía")
            return "error"
        
        print(f"[ChatGPT Service] Respuesta obtenida: {bot_response[:200]}...")
        return bot_response
        
    except Exception as e:
        print(f"[ChatGPT Service] Error: {e}")
        import traceback
        traceback.print_exc()
        return "error"
