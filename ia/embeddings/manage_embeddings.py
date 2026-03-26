# import pysqlite3
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import shutil
import threading

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

from .utils import Utils

EMBEDDINGS_LOCK = threading.Lock()

class EmbeddingsWrapper:
    """ Clase que envuelve un modelo de embeddings para que pueda ser utilizado por Chroma. 
    Coorrige error en el método embed_query. """
    def __init__(self, model):
        self.model = model

    def embed_documents(self, documents):
        """Usar el modelo original para obtener los embeddings de los documentos"""
        return self.model.embed_documents(documents)
    
    def embed_query(self, query):
        """Reutilizar el método embed_documents para queries"""
        return self.model.embed_documents([query])[0]  # Envolver la query en una lista y devolver el embedding

class EmbeddingsManager:
    def __init__(self, embedding_provider, api_key, persist_directory) -> None:
        """ Inicializa el directorio de persistencia y el modelo de embeddings. """
        self.persist_directory = persist_directory
        self.embeddings_provider = embedding_provider
        self.embeddings_model = self.initialice_embedding_model(api_key)
    
    def initialice_embedding_model(self, api_key):
        """ Define e inicializa el modelo a utilizar en la generación de embeddings. """        
        try:
            if self.embeddings_provider == "openai":
                embeddings_model = OpenAIEmbeddings(api_key=api_key, model="text-embedding-3-small")
        except Exception as e:
            print(f"Error al cargar el tipo de modelo de Embedding: {e}")
            embeddings_model = None 

        return embeddings_model

    def clear_embeddings(self) -> None:
        """Resetea la colección persistida.

        Evita borrar a nivel de filesystem (que en Azure puede dejar índices a medias
        y disparar errores tipo 'data_level0.bin' durante el rebuild).
        """
        if not self.persist_directory:
            return
        os.makedirs(self.persist_directory, exist_ok=True)

        # Reset de colección (borra y recrea la colección vacía).
        # En Azure, si el índice persistido quedó inconsistente, `reset_collection`
        # puede fallar; en ese caso hacemos fallback a borrar el folder.
        try:
            vs = Chroma(persist_directory=self.persist_directory, embedding_function=None)
            vs.reset_collection()
        except Exception as e:
            print(f"[Embeddings] reset_collection falló, aplicando fallback rmtree: {e}")
            if os.path.isdir(self.persist_directory):
                shutil.rmtree(self.persist_directory, ignore_errors=True)
            os.makedirs(self.persist_directory, exist_ok=True)
            vs = Chroma(persist_directory=self.persist_directory, embedding_function=None)
            vs.reset_collection()

    def save_embeddings(self, upload_directory, file_types) -> bool:
        """ Guarda los embeddings generados en una BD vectorial.
        Returns:
            True si se indexó al menos un fragmento; False si no había nada indexable (se vacía la BD).
        """
        with EMBEDDINGS_LOCK:
            document_chunks = Utils.load_chunked_documents(upload_directory, file_types)
            embeddings_model = EmbeddingsWrapper(self.embeddings_model)

            if not document_chunks:
                # No hay contenido indexable; evitamos vaciar la BD anterior
                # (útil si el nuevo doc es escaneado/imagen y no aporta texto).
                return False

            # Reemplazar el índice completo según el contenido actual de uploads.
            self.clear_embeddings()

            Chroma.from_documents(
                documents=document_chunks,
                embedding=embeddings_model,
                persist_directory=self.persist_directory,
            )
            return True

    def delete_vectors_for_source(self, source_filename: str) -> int:
        """Elimina de Chroma los vectores cuyo metadato ``source`` es el nombre del archivo (como al indexar)."""
        with EMBEDDINGS_LOCK:
            source = os.path.basename(source_filename)
            if (
                not source
                or not self.persist_directory
                or not os.path.isdir(self.persist_directory)
            ):
                return 0
            try:
                if not any(os.scandir(self.persist_directory)):
                    return 0
            except OSError:
                return 0
            if not self.embeddings_model:
                return 0

            wrapper = EmbeddingsWrapper(self.embeddings_model)
            vs = Chroma(
                embedding_function=wrapper,
                persist_directory=self.persist_directory,
            )

            def _ids_for_where(where: dict):
                out = vs.get(where=where)
                return out.get("ids") or []

            ids = _ids_for_where({"source": source})
            if not ids:
                ids = _ids_for_where({"source": {"$eq": source}})
            if ids:
                vs.delete(ids=ids)
            return len(ids)

    def get_embeddings(self):
        """ Obtiene los embeddings generados. """              
        with EMBEDDINGS_LOCK:
            embeddings_model_wrapper = EmbeddingsWrapper(self.embeddings_model)

            stored_embeddings = Chroma(
                embedding_function=embeddings_model_wrapper,
                persist_directory=self.persist_directory,
            )

            return stored_embeddings
