import os
from fastapi import APIRouter, FastAPI, Request, HTTPException, Response
from pydantic import BaseModel

from .utils.message_formatting import text_message
from .utils.message_processing import get_text_user, process_message, set_user_state, show_navigation_buttons, get_user_state
import apps.whatsapp.services.whatsapp_service as whatsapp_service
import apps.whatsapp.services.chatgpt_service as chatgpt_service
from base.load_env import load_env

router = APIRouter()

class Message(BaseModel):
    user_message: str
    number: str

load_env()
token_whatsapp = os.getenv("TOKEN_WHATSAPP")
api_url = os.getenv("API_URL")

def catamarca_phone_number_formateator(number):
    """ Formatea el número de teléfono de Catamarca, esto evita el error de que no llega el mensaje."""
    # Eliminar el tercer carácter
    number_temp = number[:2] + number[3:]
    # Insertar '15' entre el quinto y sexto carácter
    final_number = number_temp[:5] + '15' + number_temp[5:]
    
    return final_number

@router.get("/hola")
async def hello():
    return {"message": "Bienvenido al Bot de la Facultad de Humanidades de la UNCa."}

@router.get("/whatsapp")
async def verify_token(request: Request):
    """ Recibe una petición de Meta con el token que se cargo en su plataforma, debe ser igual al que figura en access_token. """
    try:
        access_token = "98765"
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        if token is not None and challenge is not None and token == access_token:
            return Response(content=challenge, media_type="text/plain")
        else:
            raise HTTPException(status_code=400, detail="Token o challenge no válido")
    except:
        raise HTTPException(status_code=400, detail="Ocurrio un error")
    
@router.post('/whatsapp')
async def received_message(request: Request):
    """ Recibe un mensaje del usuario en formato JSON desde WhatsApp con una estructura determinada. """
    try:
        body = await request.json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        # Verificar si hay mensajes (puede ser una notificación de estado)
        if 'messages' not in value or not value['messages']:
            # Es una notificación de estado (leído, entregado, etc.), no procesar
            return {"status": "EVENT_RECEIVED"}
        
        message = value['messages'][0]
        number = message['from']
        # Formateo el numero de teléfono para no tener problema
        number = catamarca_phone_number_formateator(number)
        
        # Verifica el tipo de mensaje que se recibe, si es texto o interactivo y retorna el texto.
        text = get_text_user(message)    
        
        # Verifica el contenido de text y de acuero a eso arma la lista de mensajes a enviar
        list_data = process_message(text, number)
        
        for item in list_data:
            # Verifica si el mensaje necesita ser procesado con ChatGPT
            needs_chatgpt = item.get("needs_chatgpt", False)
            
            if needs_chatgpt:
                # Construir el contexto de la consulta con el tema seleccionado
                query_topic = item.get("query_topic", "")
                user_query = text
                if query_topic:
                    # Agregar contexto del tema a la consulta
                    contextual_query = f"Consulta sobre {query_topic}: {user_query}"
                else:
                    contextual_query = user_query
                
                print(f"[Routes] Consulta contextual: {contextual_query}")
                responsegpt = chatgpt_service.get_bot_response(contextual_query)
                print(f"[Routes] Respuesta de ChatGPT: {responsegpt[:100] if responsegpt and responsegpt != 'error' else responsegpt}")

                if responsegpt and responsegpt != "error" and len(responsegpt.strip()) > 0:
                    # Enviar respuesta de ChatGPT
                    data = text_message(responsegpt, number)
                    result = whatsapp_service.send_message_whatsapp(data, token_whatsapp, api_url)
                    print(f"Resultado de envío de respuesta ChatGPT: {result}")
                    
                    # Obtener el estado actual para preservar la opción seleccionada
                    current_state = get_user_state(number)
                    selected_option = current_state.get("selected_option") if current_state else None
                    
                    # Cambiar estado a "waiting_feedback" preservando la opción seleccionada
                    set_user_state(number, "waiting_feedback", selected_option)
                    
                    # Mostrar botones de navegación
                    try:
                        navigation_buttons = show_navigation_buttons(number)
                        print(f"Enviando botones de navegación: {len(navigation_buttons)} botones")
                        for nav_item in navigation_buttons:
                            if nav_item.get("data"):
                                print(f"Enviando botón con data: {nav_item['data']}")
                                result_btn = whatsapp_service.send_message_whatsapp(nav_item["data"], token_whatsapp, api_url)
                                print(f"Resultado de envío de botones: {result_btn}")
                            else:
                                print("Error: nav_item no tiene data")
                    except Exception as e:
                        print(f"Error al enviar botones de navegación: {str(e)}")
                        import traceback
                        traceback.print_exc()
                else:
                    error_msg = "Ocurrió un error al procesar tu consulta. Por favor, intenta nuevamente o contacta con la secretaría."
                    print(f"[Routes] Error: respuesta de ChatGPT inválida. Valor: {responsegpt}")
                    data = text_message(error_msg, number)
                    whatsapp_service.send_message_whatsapp(data, token_whatsapp, api_url)
            elif item.get("type", False) and item.get("data"):
                # Mensaje predefinido (menú, instrucciones, etc.)
                whatsapp_service.send_message_whatsapp(item["data"], token_whatsapp, api_url)
            elif not item.get("type", True) and not needs_chatgpt:
                # Mensaje que no se reconoce pero no necesita ChatGPT
                if item.get("data"):
                    whatsapp_service.send_message_whatsapp(item["data"], token_whatsapp, api_url)
         
        return {"status": "EVENT_RECEIVED"}
    except Exception as e:
        print(f"Error en received_message: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "EVENT_RECEIVED"}
