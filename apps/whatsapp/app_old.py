from flask import Flask, request

import util
import apps.whatsapp.services.whatsapp_service as whatsapp_service
import apps.whatsapp.services.chatgpt_service as chatgpt_service


def generate_message(text, number):
    """ Genera los distintos tipo de mensajes que se pueden enviar. """

    text = text.lower()
    if "text" in text:
        data = util.text_message("Teasdasdaxt", number)
    if "format" in text:
        data = util.text_format_message(number)
    if "image" in text:
        data = util.image_message(number)
    if "audio" in text:
        data = util.audio_message(number)
    if "video" in text:
        data = util.video_message(number)
    if "document" in text:
        data = util.document_message(number)
    if "location" in text:
        data = util.location_message(number)
    if "buttons" in text:
        data = util.buttons_message(number)
    if "list" in text:
        data = util.list_message(number)

    whatsapp_service.send_message_whatsapp(data)


def process_message(text, number):
    """ Genera la interactividad con los componentes vistos. """

    text = text.lower()
    list_data = []

    if "hola" in text:
        data = util.text_message("Hola como puedo ayudarte", number)
        data_menu = util.list_message(number)
        list_data.append(data)
        list_data.append(data_menu)
    
    elif "gracias" in text:
        data = util.text_message("Gracias por contactarme", number)
        list_data.append(data)

    elif "agencia" in text:
        data = util.text_message("Esta es nuestra agencia", number)
        data_location = util.location_message(number)
        list_data.append(data)
        list_data.append(data_location)

    elif "contacto" in text:
        data = util.text_message("*Nuestro contacto:*\n4159881", number)
        list_data.append(data)
    
    elif "comprar" in text:
        data = util.buttons_message(number)             
        list_data.append(data)
    
    elif "vender" in text:
        data = util.buttons_message(number)             
        list_data.append(data)

    elif "ingresar" in text:
        data = util.text_message("Hacer click para Ingresar: https://gogole.com/", number)
        list_data.append(data)

    elif "registrarse" in text:
        data = util.text_message("Hacer click para registarse: https://google.com/", number)
        list_data.append(data)
    
    else:
        data = util.text_message("No entiendo tu mensaje", number)
        list_data.append(data)

    for item in list_data:
        whatsapp_service.send_message_whatsapp(item)


app = Flask(__name__)


@app.route('/welcome', methods=['GET'])
def index():
    """ Ruta de bienvenida a la aplicación. """
    return 'Bienvenido al sistema'


@app.route('/whatsapp', methods=['GET'])
def verify_token():
    """ Verifca el token de acceso de la aplicación. """

    try:
        access_token = "sdfsffdasfrwerwe3412"
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token != None and challenge != None and token == access_token:
            return challenge
        else:
            return "", 400
    except: 
        return "", 400   


@app.route('/whatsapp', methods=['POST'])
def received_message():
    """ Recibe la info del json pasado desde postman. """

    try:        
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']

        text = util.get_text_user(message)
        responsegpt = chatgpt_service.get_response(text)

        if responsegpt != "error":
            data = util.text_message(responsegpt, number)
        else:
            data = util.text_message("Ocurrio un error", number)
        
        whatsapp_service.send_message_whatsapp(data)


        #generate_message(text, number)
        #process_message(text, number)
        
        return "EVENT_RECEIVED"
    except:
        return "EVENT_RECEIVED"


if __name__ == '__main__':
    app.run()