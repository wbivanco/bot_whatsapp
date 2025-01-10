import os
from fastapi import APIRouter, FastAPI, Request, HTTPException
from pydantic import BaseModel

from .utils.message_formatting import text_message
from .utils.message_processing import get_text_user, process_message
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

@router.get("/whatsapp")
async def verify_token(request: Request):
    """ Recibe una petición de Meta con el token que se cargo en su plataforma, debe igual al que figura en access_token. """
    try:
        access_token = "sdfsffdasfrwerwe3412"
        token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        if token is not None and challenge is not None and token == access_token:
            return challenge
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
        message = value['messages'][0]
        number = message['from']

        # Verifica el tipo de mensaje que se recibe, si es texto o interactivo y retorna el texto.
        text = get_text_user(message)    

        # Verifica el contenido de text y de acuero a eso arma la lista de mensajes a enviar
        list_data = process_message(text, number)

        for item in list_data:
            # Verifica el contenido del mensaje y de acuerdo a eso determina si usa el chatbot o no
            if not item["type"]:  
                print("chat")
                responsegpt = chatgpt_service.get_bot_response(text)

                if responsegpt != "error":
                    data = text_message(responsegpt, number)
                else:
                    data = text_message("Ocurrio un error en el envió del mensaje", number)
            else:
                data = item["data"]
            whatsapp_service.send_message_whatsapp(data, token_whatsapp, api_url)
         
        return {"status": "EVENT_RECEIVED"}
    except:
        return {"status": "EVENT_RECEIVED"}
