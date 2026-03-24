import os
from typing import Optional

from ia.llm.manage_llm import LlmManager
from ia.embeddings.manage_embeddings import EmbeddingsManager

from base.load_env import load_env

load_env()
api_key = os.getenv("OPENAI_API_KEY")
persist_directory = os.getenv("PERSIST_CHROMADB_FOLDER")

def get_bot_response(llm_query: str, retrieval_query: Optional[str] = None):
    """Obtiene la respuesta del bot usando RAG.

    Args:
        llm_query: Texto que ve el modelo (puede incluir contexto del menú).
        retrieval_query: Texto usado solo para búsqueda vectorial; si es None, se usa llm_query.
    """
    r_query = (retrieval_query if retrieval_query is not None else llm_query).strip()
    try:
        print(f"[ChatGPT Service] Procesando consulta (LLM): {llm_query}")
        print(f"[ChatGPT Service] Búsqueda vectorial con: {r_query!r}")
        
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
        
        try:
            n_stored = stored_embeddings._collection.count()
        except Exception as exc:
            n_stored = -1
            print(f"[ChatGPT Service] No se pudo leer el conteo de Chroma: {exc}")
        print(f"[ChatGPT Service] Registros en colección Chroma: {n_stored}")
        if n_stored == 0:
            print(
                "[ChatGPT Service] La colección vectorial está vacía. "
                "Subí documentos desde el panel y generá embeddings; en Azure el disco local suele no persistir entre reinicios "
                "salvo que uses almacenamiento persistente o vuelvas a generar índice en el servidor."
            )

        retriever = stored_embeddings.as_retriever(
            search_type="similarity", search_kwargs={"k": 10}
        )
        docs = retriever.invoke(r_query)
        print(f"[ChatGPT Service] Documentos recuperados: {len(docs)}")
        for i, doc in enumerate(docs):
            print(f"[ChatGPT Service] Doc {i+1}: {doc.metadata.get('source', 'Sin fuente')}")
            preview = (doc.page_content or "")[:200]
            print(f"[ChatGPT Service] Contenido: {preview}...")

        context = "\n\n".join(
            d.page_content for d in docs if d.page_content and d.page_content.strip()
        )
        bot_response = llm_manager.answer_rag_stuff(llm, context, llm_query)
        
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
