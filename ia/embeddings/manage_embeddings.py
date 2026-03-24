# import pysqlite3
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import shutil

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

from .utils import Utils

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
        """Elimina la colección persistida. Útil cuando no quedan documentos indexables."""
        if not self.persist_directory:
            return
        if os.path.isdir(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        os.makedirs(self.persist_directory, exist_ok=True)

    def save_embeddings(self, upload_directory, file_types) -> bool:
        """ Guarda los embeddings generados en una BD vectorial.
        Returns:
            True si se indexó al menos un fragmento; False si no había nada indexable (se vacía la BD).
        """
        document_chunks = Utils.load_chunked_documents(upload_directory, file_types)
        embeddings_model = EmbeddingsWrapper(self.embeddings_model)

        if not document_chunks:
            self.clear_embeddings()
            return False

        # Reemplazar el índice completo según el contenido actual de uploads (evita duplicados y estados viejos).
        self.clear_embeddings()

        Chroma.from_documents(
            documents=document_chunks, 
            embedding=embeddings_model, 
            persist_directory=self.persist_directory
        )
        return True

    def delete_vectors_for_source(self, source_filename: str) -> int:
        """Elimina de Chroma los vectores cuyo metadato ``source`` es el nombre del archivo (como al indexar)."""
        source = os.path.basename(source_filename)
        if not source or not self.persist_directory or not os.path.isdir(self.persist_directory):
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
        embeddings_model_wrapper = EmbeddingsWrapper(self.embeddings_model)  

        stored_embeddings = Chroma(
            embedding_function=embeddings_model_wrapper, 
            persist_directory=self.persist_directory
        )

        return stored_embeddings
