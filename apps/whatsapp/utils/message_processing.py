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
    saludos = ["hola", "buenas", "qué tal", "saludos", "buenos días", "buenas tardes", "buenas noches", "buen día", 
               "buen dia", "como estás", "como estas", "como andas", "como andás", "como andas?", "como andás?",]
    despedidas = ["gracias", "muchas gracias", "adiós", "nos vemos", "hasta luego", "chau", "hasta pronto"]
    
    materias = ["materias", "reinscripciones", "reinscripción", "reinscripcion"]
    examenes = ["exámenes", "examenes", "examen"]
    

    if find_whole_word(text, saludos):
        #data_buttons = mf.buttons_message(number, "Escribí el número o palabra clave de la opción que necesitás", buttons=["1 - Inscripciones", "2 - Reinscripciones", "3 - Exámenes"])
        # data_options = mf.text_message("Escribí el número o palabra clave de la opción que necesitás: \n\n" \
        # "1 Inscripciones e Ingreso 2025\n" \
        # "2 Reinscripciones y Materias \n" \
        # "3 Exámenes Finales\n" \
        # "4 Equivalencias \n" \
        # "5 Título, Colación y Egresos \n" \
        # "6 Calendario Académico \n" \
        # "7 Oferta Académica \n" \
        # "8 Reglamento de Alumnos \n" \
        # "9 Contactos y Enlaces Utiles \n" \
        data = mf.text_message("Hola, soy HumaChat tu asistente virtual de la Facultad de Humanidades.", number)
        sections = [
            {
                "title": "Calendario Académico",
                "rows": [
                    {
                        "id": "calendario-academico",
                        "title": "Calendario 2025",
                        "description": "Informacion de fechas académicas"
                    }
                ]
            },
            {
                "title": "Reglamentos/Instructivos",
                "rows": [
                    {
                        "id": "reglamento-alumnos",
                        "title": "Reglamento de Alumnos",
                        "description": "Aquí puede ir una breve descripción"
                    },
                    {
                        "id": "instructivo-inscripcion",
                        "title": "Instructivo Inscripción",
                        "description": "Aquí puede ir una breve descripción"
                    }
                ]
            },
            {
                "title": "Prácticas",
                "rows": [
                    {
                        "id": "practicas",
                        "title": "Cursar Práctica Docente",
                        "description": "Aquí puede ir una breve descripción"
                    }
                ]
            }
        ]
        data_options = mf.list_message(number, sections)
        list_data.append({'data': data, 'type': True})
        list_data.append({'data': data_options, 'type': True}) 

    elif find_whole_word(text, materias):
        data = mf.text_message("📚 REINSCRIPCIONES Y MATERIAS\n\n" \
            "🔁 Reinscripción anual: 10/02 al 17/03/2025\n" \
            "📌 Materias anuales y primer cuatrimestre: 19/03 al 28/03\n" \
            "📌 Segundo cuatrimestre: 11/08 al 22/08\n" \
            "📍 Recordá tener aprobadas las correlativas.\n" \
            "📋 Info completa en la Guía de Trámites", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, examenes):
        data = mf.text_message("📝 EXÁMENES FINALES\n\n" \
            "🗓️ Turnos Ordinarios 2025:\n" \
            "▪ Febrero-Marzo: 1° 17/02 a 21/02 – 2° 10/03 a 14/03\n" \
            "▪ Julio-Agosto: 1° 3/07 a 10/07– 2° 4/08 a 08/08\n" \
            "▪ Noviembre-Diciembre 24/11 a 28/11 – 2° 12/12 a 18/12\n" \
            "🛑 Inscripción obligatoria 2 días antes\n" \
            "📖 Mesas especiales: hasta 2 materias para egresar\n" \
            "🔎 Consultá fechas exactas y reglamento en la Guía", number)
        list_data.append({'data': data, 'type': True})
    
    elif find_whole_word(text, despedidas):
        data = mf.text_message("Muchas gracias por haberte comunicado", number)
        list_data.append({'data': data, 'type': True})
    else:
        data = mf.text_message("Lo siento pero no entiendo tu mensaje", number)
        list_data.append({'data':data, 'type': False})

    return list_data
