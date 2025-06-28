from . import message_formatting as mf
import re

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

def find_whole_word(text, keywords):
    """Busca coincidencias de palabras completas en el texto."""
    return any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords)

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

    # Ordenamos las keywords de más específicas a más generales
    posgrado_keywords = ["posgrado", "postgrado", "postgrados", "posgrado", "maestría", "maestrías",
                         "maestria", "maestrias", "especialización", "especiacializaciones", 
                         "doctorado", "doctorados"]
    diplomaturas_keywords = ["diplomatura", "diplomaturas"]
    grado_keywords = ["carreras de grado", "licenciatura", "licenciaturas", "grado", "profesorado", "profesorados"]
    saludos = ["hola", "buenas", "qué tal", "saludos", "buenos días", "buenas tardes", "buenas noches", "buen día", 
               "buen dia", "como estás", "como estas", "como andas", "como andás", "como andas?", "como andás?",]
    despedidas = ["gracias", "muchas gracias", "adiós", "nos vemos", "hasta luego", "chau", "hasta pronto"]
    autoridades = ["autoridades", "autoridad", "autoridad de la facultad", "autoridades de la facultad"]
    ingreso = ["ingreso", "ingresantes", "ingresantes 2025"]
    centro_estudiantes = ["centro de estudiantes", "centro de estudiantes de la facultad", "centro de estudiantes de la facultad de humanidades"]
    siu = ["siu", "siu guarani", "siu guaraní", "acceso siu", "acceso siu guaraní", "acceso siu guarani"]

    if find_whole_word(text, saludos):
        data = mf.text_message("Hola soy HumaChat tu asistente virtual de la Facultad de Humanidades", number)
        data_buttons = mf.buttons_message(number, "Escribi el número o palabra clave de la opción que necesitas", buttons=["1 - Inscripciones e Ingresi 2025", "2 -Reinscripciones y Materias", "3 - Exámenes Finales"])
        list_data.append({'data': data, 'type': True})
        list_data.append({'data': data_buttons, 'type': True}) 
    elif find_whole_word(text, posgrado_keywords):
        data = mf.text_message("Listado de la carreras de posgrado: https://huma.unca.edu.ar/oferta-academica/posgrado", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, diplomaturas_keywords):
        data = mf.text_message("Listado de la carreras de diplomaturas: https://huma.unca.edu.ar/oferta-academica/diplomaturas", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, grado_keywords):
        data = mf.text_message("Listado de la carreras de grado: https://huma.unca.edu.ar/oferta-academica/grado", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, autoridades):
        data = mf.text_message("Autoridades de la Facultad: https://huma.unca.edu.ar/institucional/autoridades", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, ingreso):
        data = mf.text_message("Información para los ingresantes: https://huma.unca.edu.ar/alumnos/ingreso-2025", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, centro_estudiantes):
        data = mf.text_message("Información de Interés de Centro de estudiantes: https://huma.unca.edu.ar/alumnos/centro-de-estudiantes", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, siu):
        data = mf.text_message("Acceso al SIU Guaraní: https://guarani.unca.edu.ar/", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, despedidas):
        data = mf.text_message("Muchas gracias por haberte comunicado", number)
        list_data.append({'data': data, 'type': True})
    else:
        data = mf.text_message("Lo siento pero no entiendo tu mensaje", number)
        list_data.append({'data':data, 'type': False})

    return list_data
