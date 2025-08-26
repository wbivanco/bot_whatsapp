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
    # posgrado_keywords = ["posgrado", "postgrado", "postgrados", "posgrado", "maestría", "maestrías",
    #                      "maestria", "maestrias", "especialización", "especiacializaciones", 
    #                      "doctorado", "doctorados"]
    # diplomaturas_keywords = ["diplomatura", "diplomaturas"]
    # grado_keywords = ["carreras de grado", "licenciatura", "licenciaturas", "grado", "profesorado", "profesorados"]
    # autoridades = ["autoridades", "autoridad", "autoridad de la facultad", "autoridades de la facultad"]
    # ingreso = ["ingreso", "ingresantes", "ingresantes 2025"]
    # centro_estudiantes = ["centro de estudiantes", "centro de estudiantes de la facultad", "centro de estudiantes de la facultad de humanidades"]
    # siu = ["siu", "siu guarani", "siu guaraní", "acceso siu", "acceso siu guaraní", "acceso siu guarani"]

    saludos = ["hola", "buenas", "qué tal", "saludos", "buenos días", "buenas tardes", "buenas noches", "buen día", 
               "buen dia", "como estás", "como estas", "como andas", "como andás", "como andas?", "como andás?",]
    despedidas = ["gracias", "muchas gracias", "adiós", "nos vemos", "hasta luego", "chau", "hasta pronto"]
    inscripciones = ["inscripciones", "inscripción", "inscripcion", "ingreso 2025", "ingreso 2023", "1"]
    materias = ["materias", "reinscripciones", "reinscripción", "reinscripcion", "2"]
    examenes = ["exámenes", "examenes", "examen", "3"]
    equivalencias = ["equivalencias", "4"]
    titulo = ["título", "colación", "egresos", "5"]
    calendario = ["calendario", "calendario académico", "6"]
    oferta_academica = ["oferta académica", "oferta academica", "oferta", "7"]
    reglamento = ["reglamento de alumnos", "reglamento", "reglamento alumnos", "8"]
    contactos = ["contactos", "enlaces útiles", "enlaces utiles", "contactos y enlaces utiles", "contactos y enlaces útiles", "9"]
    

    if find_whole_word(text, saludos):
        data = mf.text_message("Hola, soy HumaChat tu asistente virtual de la Facultad de Humanidades.", number)
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
        # , number)
        sections = [
            {
                "title": "Calendario Académico",
                "rows": [
                    {
                        "id": "calendario-inicio",
                        "title": "Inicio y Finalización de",
                        "description": "Aquí puede ir una breve descripción"
                    },
                    {
                        "id": "calendario-inscripciones",
                        "title": "Inscripciones 1° Año de ",
                        "description": "Aquí puede ir una breve descripción"
                    }
                ]
            },
            {
                "title": "Reglamento de Alumnos",
                "rows": [
                    {
                        "id": "reglamento-adminsion",
                        "title": "Regimen de Admisión del2",
                        "description": "Aquí puede ir una breve descripción"
                    },
                    {
                        "id": "reglamento-readmicion",
                        "title": "Regimen de Readmición",
                        "description": "Aquí puede ir una breve descripción"
                    }
                ]
            },
            {
                "title": "Instructivo Inscripción",
                "rows": [
                    {
                        "id": "ingreso",
                        "title": "Como Inscribirse",
                        "description": "Aquí puede ir una breve descripción"
                    }
                ]
            }
        ]
        data_options = mf.list_message(number, sections)
        list_data.append({'data': data, 'type': True})
        list_data.append({'data': data_options, 'type': True}) 
    elif find_whole_word(text, inscripciones):  
        data = mf.text_message("🧾 1 INSCRIPCIONES E INGRESO 2025\n\n" \
            "🗓️ Preinscripción online: 09/12/2024 al 05/03/2025\n" \
            "📄 Entrega de documentación: 17/03 al 30/04/2025\n" \
            "📜 Título secundario: hasta el 30/09/2025\n" \
            "👥 Mayores de 25 años (Ley 24.521): inscripción especial + examen de admisión\n" \
            "🎓 M.A.C. (Curso de ingreso): 10 al 14 de marzo de 2025\n" \
            "🔗 Más info: Guía de trámites https://huma.unca.edu.ar/oferta-academica", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, materias):
        data = mf.text_message("📚 2 REINSCRIPCIONES Y MATERIAS\n\n" \
            "🔁 Reinscripción anual: 10/02 al 17/03/2025\n" \
            "📌 Materias anuales y primer cuatrimestre: 19/03 al 28/03\n" \
            "📌 Segundo cuatrimestre: 11/08 al 22/08\n" \
            "📍 Recordá tener aprobadas las correlativas.\n" \
            "📋 Info completa en la Guía de Trámites", number)
        list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, examenes):
        data = mf.text_message("📝 3 EXÁMENES FINALES\n\n" \
        "🗓️ Turnos Ordinarios 2025:\n" \
        "▪ Febrero-Marzo: 1° 17/02 a 21/02 – 2° 10/03 a 14/03\n" \
        "▪ Julio-Agosto: 1° 3/07 a 10/07– 2° 4/08 a 08/08\n" \
        "▪ Noviembre-Diciembre 24/11 a 28/11 – 2° 12/12 a 18/12\n" \
        "🛑 Inscripción obligatoria 2 días antes\n" \
        "📖 Mesas especiales: hasta 2 materias para egresar\n" \
        "🔎 Consultá fechas exactas y reglamento en la Guía", number)
        list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, posgrado_keywords):
    #     data = mf.text_message("Listado de la carreras de posgrado: https://huma.unca.edu.ar/oferta-academica/posgrado", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, diplomaturas_keywords):
    #     data = mf.text_message("Listado de la carreras de diplomaturas: https://huma.unca.edu.ar/oferta-academica/diplomaturas", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, grado_keywords):
    #     data = mf.text_message("Listado de la carreras de grado: https://huma.unca.edu.ar/oferta-academica/grado", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, autoridades):
    #     data = mf.text_message("Autoridades de la Facultad: https://huma.unca.edu.ar/institucional/autoridades", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, ingreso):
    #     data = mf.text_message("Información para los ingresantes: https://huma.unca.edu.ar/alumnos/ingreso-2025", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, centro_estudiantes):
    #     data = mf.text_message("Información de Interés de Centro de estudiantes: https://huma.unca.edu.ar/alumnos/centro-de-estudiantes", number)
    #     list_data.append({'data': data, 'type': True})
    # elif find_whole_word(text, siu):
    #     data = mf.text_message("Acceso al SIU Guaraní: https://guarani.unca.edu.ar/", number)
    #     list_data.append({'data': data, 'type': True})
    elif find_whole_word(text, despedidas):
        data = mf.text_message("Muchas gracias por haberte comunicado", number)
        list_data.append({'data': data, 'type': True})
    else:
        data = mf.text_message("Lo siento pero no entiendo tu mensaje", number)
        list_data.append({'data':data, 'type': False})

    return list_data
