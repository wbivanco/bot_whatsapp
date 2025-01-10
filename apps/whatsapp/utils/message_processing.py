from . import message_formatting as mf

def get_text_user(message):
    """ Verifica el tipo de mensaje que se recibe, si es texto o interactivo y retorna el 
    texto. """
    text = ""
    type_message = message['type']

    if type_message == 'text':
        text = message['text']['body']
    elif type_message == 'interactive':
        interactive_object = message['interactive']
        type_interactive = interactive_object['type']

        if type_interactive == 'button_reply':
            text = interactive_object['button_reply']['title']
        elif type_interactive == 'list_reply':
            text = interactive_object['list_reply']['title']
        else:
            print("No es de tipo interactivo el mensaje")
    else:
        print("No es de tipo texto el mensaje")

    return text

def process_message(text, number):
    """ Verifica el contenidp de la variables text y de acuerdo a ello arma la lista de diccionarios, si en el texto no está
    algunas de las palabra que se chequea en los if, es decir sale por else, se agrega la clave type con el valor False. 
    Ejemplos de como armar la lista de diccionarios:s
        data = mf.text_message("*Hola como puedo ayudarte*", number)
        data = mf.text_message("*Nuestro contacto:*\n4159881", number)
        data = mf.text_message("Hacer click para Ingresar: https://gogole.com/", number)
        data_menu = mf.list_message(number)
        data_location = mf.location_message(number)
        data_buttons = mf.buttons_message(number)          
        
        list_data.append(data)
        list_data.append(data_menu)
        list_data.append(data_location)
        list_data.append(data_buttons)
    """
    text = text.lower()
    list_data = []

    saludos = ["hola", "buenas", "qué tal", "saludos"]
    grado_keywords = ["grado", "carreras de grado", "universitario", "licenciatura"]
    posgrado_keywords = ["posgrado", "maestría", "doctorado", "postgrado"]
    diplomaturas_keywords = ["diplomatura", "especialización", "curso corto"]
    despedidas = ["gracias", "muchas gracias", "adiós", "nos vemos"]

    if any(kw in text for kw in saludos):
       data = mf.text_message("Hola como puedo ayudarte", number)
       data_buttons = mf.buttons_message(number, "Nuestra propuesta", buttons=["Grado", "Posgrado", "Diplomaturas"])
       list_data.append({'data': data, 'type': True})
       list_data.append({'data': data_buttons, 'type': True}) 
    elif any(kw in text for kw in grado_keywords):
        data = mf.text_message("Listado de la carreras de grado: https://huma.unca.edu.ar/oferta-academica/grado", number)
        list_data.append({'data': data, 'type': True})
    elif any(kw in text for kw in posgrado_keywords):
        data = mf.text_message("Listado de la carreras de posgrado: https://huma.unca.edu.ar/oferta-academica/posgrado", number)
        list_data.append({'data': data, 'type': True})
    elif any(kw in text for kw in diplomaturas_keywords):
        data = mf.text_message("Listado de la carreras de diplomaturas: https://huma.unca.edu.ar/oferta-academica/diplomaturas", number)
        list_data.append({'data': data, 'type': True})
    elif any(kw in text for kw in despedidas):
        data = mf.text_message("Muchas gracias por haberte comunicado", number)
        list_data.append({'data': data, 'type': True})
    else:
        data = mf.text_message("Lo siento pero no entiendo tu mensaje", number)
        list_data.append({'data':data, 'type': False})

    return list_data
