from typing import Any
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

RAG_STUFF_PROMPT = PromptTemplate(
    template="""Eres un asistente amigable y servicial para la Facultad de Humanidades de la Universidad Nacional de Catamarca.

REGLAS CRÍTICAS:
1. DEBES responder ÚNICAMENTE con la información que está en los siguientes documentos de contexto
2. SIEMPRE responde en español argentino con tono cálido y amigable
3. NUNCA digas "no sé", "no tengo información" o "no está en los documentos" sin haber analizado exhaustivamente el contexto
4. Si la información no está exactamente en los documentos pero hay información relacionada, compártela de forma útil
5. Si realmente no hay información relevante, ofrece ayuda con otros temas relacionados que sí tengas

CONTEXTO (información de los documentos):
{context}

PREGUNTA DEL USUARIO: {question}

INSTRUCCIONES:
- Analiza cuidadosamente el contexto proporcionado
- Extrae la información relevante para responder la pregunta
- Si encuentras información relacionada aunque no sea exactamente lo que preguntan, compártela
- Responde de forma clara, amigable y en español argentino
- Si tu respuesta es completa, termínala ahí. Si crees que el usuario podría tener más dudas, agrega al final: "🤔 ¿Te queda alguna duda sobre este tema?"

RESPUESTA:""",
    input_variables=["context", "question"],
)


class LlmManager:
    """ Clase que maneja la carga y configuración de modelos de lenguaje y conversación. """  
    def __init__(self, llm_provider) -> None:
        self.llm_provider = llm_provider
    
    def initialice_llm_model(self, model_name, api_key, temperature=0):
        """ Carga el modelo y el api_key de OpenAI(pasados como parámetros obligatorios) y lo inicializa con la 
        temperatura deseada(por defecto es cero), se debe pasar el provider(empresa) del modelo, que indica que 
        clase de langchain se debe llamar.
        
        Args:
            model_name (str): Nombre del modelo.
            openai_api_key (str): Clave de API.
            temperature (float, optional): Temperatura del modelo. Por defecto es 0.
            system_prompt (str, optional): Prompt del sistema para inicializar el modelo. Por defecto es None.
    
        Returns:
            llm: Instancia del modelo inicializado. 
        """
       
        try:
            if self.llm_provider == "openai":
                llm = ChatOpenAI(                    
                    model_name=model_name, 
                    api_key=api_key,
                    temperature=temperature,                   
                )
        except Exception as e:
            print(f"Error al cargar el tipo de modelo LLM: {e}")
            llm = None    

        return llm
    
    def initialice_retriever(self, llm, stored_embeddings, search_type="similarity", num_result=1):
        """ Inicializa el modelo de recuperación de información, pasando el modelo de lenguaje y los embeddings, 
        ademas se pueden pasar como parámetros el tipo de búsqueda y la cantidad de resultados, ambos opcionales. """

        retriever = stored_embeddings.as_retriever(search_type=search_type, search_kwargs={"k": num_result})
        
        QA_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": RAG_STUFF_PROMPT},
        )

        return QA_chain

    def answer_rag_stuff(self, llm, context: str, question: str) -> str:
        """Responde con el mismo prompt que RetrievalQA stuff, sin volver a ejecutar el retriever."""
        chain = RAG_STUFF_PROMPT | llm
        out = chain.invoke({"context": context or "(sin documentos recuperados)", "question": question})
        return out.content if getattr(out, "content", None) else str(out)

    def get_response_retriever(self, QA_chain, user_message, history):
        """ Recibe la cadena con el llm y retriever, además de la pregunta del usuario y el historial del chat, devuelve \
            la respuesta del bot, de donde saco la información y el historial. """
        messages = [
            SystemMessage(
                content="""Eres un asistente amigable y servicial para la Facultad de Humanidades de la Universidad Nacional de Catamarca.

REGLAS IMPORTANTES:
1. SOLO responde con información que esté en los documentos PDF proporcionados
2. SIEMPRE responde en castellano (español argentino)
3. Usa un tono cálido, amigable y cercano como si hablaras con un amigo
4. Si no tienes la información específica, NO digas simplemente "no sé"
5. En lugar de "no sé", responde de forma amigable como: "¡Hola! Esa información específica no la tengo en mis documentos, pero puedo ayudarte con otros trámites de la facultad. ¿Te interesa saber sobre [menciona algún tema relacionado que sí tengas]?"

TU ROL:
- Ayudar a estudiantes con trámites administrativos
- Brindar información sobre gestión académica
- Orientar sobre vida universitaria
- Ser empático y comprensivo con las dudas de los jóvenes

RECUERDA: Eres un compañero que quiere ayudar, no un robot frío. Usa emojis ocasionalmente y mantén un lenguaje cercano pero respetuoso.

DESPUÉS DE CADA RESPUESTA:
- Si tu respuesta es completa y clara, termina ahí
- Si tu respuesta podría no ser suficiente o si crees que el usuario podría tener más dudas, agrega al final:
  "¿Te queda alguna duda sobre este tema o necesitas información sobre algo más?"
- Usa emojis para hacer la pregunta más amigable, por ejemplo: "🤔 ¿Te queda alguna duda sobre este tema o necesitas información sobre algo más?" """
            ),  # System prompt
        ]

        # Agregar el historial de mensajes
        for msg in history:            
            messages.append(HumanMessage(content=msg["user"]))
            messages.append(HumanMessage(content=msg["assistant"]))   

        # Agregar el mensaje actual del usuario
        messages.append(HumanMessage(content=user_message))

        response = QA_chain.invoke({"query": user_message, "messages": messages})
        bot_response = response["result"]
        source_documents = response["source_documents"]
        
        # Extraer fuentes con metadatos adicionales (ej. título, enlace)
        sources = []
        for doc in source_documents:
            source_info = {
                'source': doc.metadata.get('source', 'Desconocido'),  # Fuente original
                'title': doc.metadata.get('title', 'Sin título'),  # Título del documento
                'url': doc.metadata.get('url', ''),  # Enlace si está disponible
                'snippet': doc.page_content[:200]  # Primeros 200 caracteres del documento
            }
            sources.append(source_info)
  
        return bot_response, sources

    def get_response_retriever_without_memory(self, QA_chain, user_message):
        """ Recibe la cadena con el llm y retriever y la pregunta del usuario, devuelve solo la respuesta del bot. 
        El prompt template personalizado ya está configurado en initialice_retriever, así que solo necesitamos pasar la query."""
        response = QA_chain.invoke({"query": user_message})
        bot_response = response["result"]
    
        return bot_response