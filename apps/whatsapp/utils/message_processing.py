from . import message_formatting as mf
import re

# Diccionario global para almacenar el estado de cada usuario (número de teléfono -> estado)
user_states = {}

def get_text_user(message):
    """ Verifica el tipo de mensaje que se recibe, si es texto o interactivo y retorna el 
    texto. Para listas interactivas, retorna el ID en lugar del título para mejor procesamiento. """
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
            # Retornar el ID en lugar del título para mejor identificación
            text = interactive_object['list_reply']['id']
        else:
            print("No es de tipo interactivo el mensaje")
    else:
        print("No es de tipo texto el mensaje")

    return text

def find_whole_word(text, keywords):
    """Busca coincidencias de palabras completas en el texto."""
    return any(re.search(r'\b' + re.escape(kw) + r'\b', text) for kw in keywords)

def get_user_state(number):
    """Obtiene el estado actual del usuario. Si no existe, retorna None."""
    return user_states.get(number)

def set_user_state(number, state, selected_option=None):
    """Establece el estado del usuario."""
    user_states[number] = {
        "state": state,
        "selected_option": selected_option
    }

def clear_user_state(number):
    """Limpia el estado del usuario."""
    if number in user_states:
        del user_states[number]

# Texto fijo antes de pedir la consulta (p. ej. horarios de atención presencial).
# Enunciado informativo: no hace falta mencionar qué canales no están disponibles.
MSG_HORARIOS_DIVISION_ALUMNOS = (
    "📌 *División Alumnos — horarios de atención*\n"
    "• Mañana: 8 a 12 h\n"
    "• Tarde: 16 a 20 h"
)

def get_option_name(option_id):
    """Mapea el ID de la opción a su nombre descriptivo."""
    options_map = {
        "inscripciones-2026": "Inscripciones e Ingreso 2026",
        "reinscripciones-materias": "Reinscripciones y Materias",
        "examenes-finales": "Exámenes Finales",
        "equivalencias": "Equivalencias",
        "titulo-colacion": "Título, Colación y Egresos",
        "calendario-academico": "Calendario Académico",
        "oferta-academica": "Oferta Académica",
        "reglamento-alumnos": "Reglamento de Alumnos",
        "contacto": "Contactos y Enlaces Útiles",
        "otras-consultas": "Otras Consultas"
    }
    return options_map.get(option_id, "tu consulta")

def show_main_menu(number):
    """Muestra el menú principal."""
    data = mf.text_message("¡Hola! 👋 Soy HumaBot, el asistente virtual de la Facultad de Humanidades de la UNCa. Estoy acá para ayudarte con tus consultas sobre trámites, fechas importantes, materias y todo lo que necesites de la facu 😊💬", number)
    sections = [
        {
            "title": "HumaChat",
            "rows": [
                {
                    "id": "inscripciones-2026",
                    "title": "Inscripción/Ingreso 2026",
                },
                {
                    "id": "reinscripciones-materias",
                    "title": "Reinscripción y Materias",
                },
                {
                    "id": "examenes-finales",
                    "title": "Exámenes Finales",
                },
                {
                    "id": "equivalencias",
                    "title": "Equivalencias",
                },
                {
                    "id": "titulo-colacion",
                    "title": "Título, Colación, Egreso",
                },
                {
                    "id": "calendario-academico",
                    "title": "Calendario Académico",
                },
                {
                    "id": "oferta-academica",
                    "title": "Oferta Académica",
                },
                {
                    "id": "reglamento-alumnos",
                    "title": "Reglamentos de Alumnos",
                },
                {
                    "id": "contacto",
                    "title": "Contacto, Enlaces Utiles",
                },
                {
                    "id": "otras-consultas",
                    "title": "Otras Consultas",
                }
            ]
        }
    ]
    data_options = mf.list_message(number, sections)
    return [{'data': data, 'type': True}, {'data': data_options, 'type': True}]

def show_navigation_buttons(number):
    """Muestra los botones de navegación después de una respuesta.
    Nota: Los títulos de botones deben tener máximo 20 caracteres según WhatsApp."""
    # Textos acortados para cumplir con el límite de 20 caracteres de WhatsApp
    buttons = [
        "Sí, resolví consulta",  # 20 caracteres ✓
        "No, otra pregunta",  # 18 caracteres ✓
        "🔙 Menú Principal"  # 18 caracteres ✓
    ]
    data = mf.buttons_message(number, "¿Logramos resolver tu consulta?", buttons)
    return [{'data': data, 'type': True}]

def process_message(text, number):
    """ Procesa el mensaje del usuario según el estado de la conversación y retorna la lista de mensajes a enviar.
    
    Estados posibles:
    - None: Usuario nuevo o sin estado
    - "menu": Usuario está en el menú principal
    - "waiting_query": Usuario seleccionó una opción y está esperando su consulta
    - "waiting_feedback": Usuario recibió respuesta y está esperando feedback
    
    Retorna una lista de diccionarios con la estructura:
    [{'data': {...}, 'type': True/False, 'needs_chatgpt': True/False, 'query_topic': 'tema'}]
    donde:
    - 'data': datos del mensaje a enviar
    - 'type': True si es mensaje predefinido, False si necesita procesamiento con ChatGPT
    - 'needs_chatgpt': True si el mensaje necesita ser procesado con ChatGPT
    - 'query_topic': tema de la consulta (para contexto)
    """
    text_lower = text.lower()
    text_original = text  # Mantener texto original para comparaciones exactas
    list_data = []
    user_state = get_user_state(number)

    # Keywords para reconocimiento
    saludos = ["hola", "buenas", "qué tal", "saludos", "buenos días", "buenas tardes", "buenas noches", "buen día", 
               "buen dia", "como estás", "como estas", "como andas", "como andás", "como andas?", "como andás?"]
    
    # Mapeo de opciones del menú
    option_map = {
        "inscripciones-2026": "Inscripciones e Ingreso 2026",
        "reinscripciones-materias": "Reinscripciones y Materias",
        "examenes-finales": "Exámenes Finales",
        "equivalencias": "Equivalencias",
        "titulo-colacion": "Título, Colación y Egresos",
        "calendario-academico": "Calendario Académico",
        "oferta-academica": "Oferta Académica",
        "reglamento-alumnos": "Reglamento de Alumnos",
        "contacto": "Contactos y Enlaces Útiles",
        "otras-consultas": "Otras Consultas"
    }
    
    # Mapeo de números a IDs de opciones
    number_to_option = {
        "1": "inscripciones-2026",
        "2": "reinscripciones-materias",
        "3": "examenes-finales",
        "4": "equivalencias",
        "5": "titulo-colacion",
        "6": "calendario-academico",
        "7": "oferta-academica",
        "8": "reglamento-alumnos",
        "9": "contacto",
        "10": "otras-consultas"
    }

    # Manejar botones de navegación (actualizados con textos acortados)
    if text_original == "Sí, resolví consulta":
        data = mf.text_message("Gracias por comunicarte. Estoy aquí para ayudarte con cualquier consulta sobre tramites de la Facultad de Humanidades – UNCA", number)
        list_data.append({'data': data, 'type': True, 'needs_chatgpt': False})
        clear_user_state(number)
        return list_data
    
    elif text_original == "No, otra pregunta":
        if user_state and user_state.get("selected_option"):
            option_name = get_option_name(user_state["selected_option"])
            data = mf.text_message(f"📋 Escribí tu consulta respecto de \"{option_name}\"", number)
            set_user_state(number, "waiting_query", user_state["selected_option"])
            list_data.append({'data': data, 'type': True, 'needs_chatgpt': False})
        else:
            # Si no hay opción seleccionada, volver al menú
            list_data.extend(show_main_menu(number))
            set_user_state(number, "menu")
        return list_data
    
    elif text_original == "🔙 Menú Principal":
        list_data.extend(show_main_menu(number))
        set_user_state(number, "menu")
        return list_data

    # Si el usuario está esperando feedback, cualquier mensaje que no sea un botón vuelve al menú
    if user_state and user_state.get("state") == "waiting_feedback":
        if not (text_original in ["Sí, resolví consulta", "No, otra pregunta", "🔙 Menú Principal"]):
            list_data.extend(show_main_menu(number))
            set_user_state(number, "menu")
            return list_data

    # Si el usuario está esperando una consulta, procesar con ChatGPT
    if user_state and user_state.get("state") == "waiting_query":
        # Este mensaje será procesado con ChatGPT
        option_name = get_option_name(user_state["selected_option"])
        list_data.append({
            'data': None,  # Se generará después con la respuesta de ChatGPT
            'type': False, 
            'needs_chatgpt': True,
            'query_topic': option_name
        })
        return list_data

    # Manejar saludos - mostrar menú principal
    if find_whole_word(text_lower, saludos) or not user_state:
        list_data.extend(show_main_menu(number))
        set_user_state(number, "menu")
        return list_data

    # Manejar selección de opciones del menú (por ID o por número)
    selected_option_id = None
    
    # Verificar si es un ID de opción del menú
    if text_original in option_map:
        selected_option_id = text_original
    # Verificar si es un número (1-10)
    elif text_original in number_to_option:
        selected_option_id = number_to_option[text_original]
    # Verificar si el texto coincide con algún título de opción
    else:
        for option_id, option_name in option_map.items():
            if option_name.lower() in text_lower or text_original in option_name:
                selected_option_id = option_id
                break

    if selected_option_id:
        option_name = option_map[selected_option_id]
        if selected_option_id == "contacto":
            list_data.append(
                {
                    "data": mf.text_message(MSG_HORARIOS_DIVISION_ALUMNOS, number),
                    "type": True,
                    "needs_chatgpt": False,
                }
            )
        data = mf.text_message(f"📋 Escribí tu consulta respecto de \"{option_name}\"", number)
        list_data.append({'data': data, 'type': True, 'needs_chatgpt': False})
        set_user_state(number, "waiting_query", selected_option_id)
        return list_data

    # Si no se reconoce el mensaje y el usuario está en el menú, mostrar menú nuevamente
    if user_state and user_state.get("state") == "menu":
        data = mf.text_message("No entendí tu mensaje. Por favor, selecciona una opción del menú.", number)
        list_data.append({'data': data, 'type': True, 'needs_chatgpt': False})
        list_data.extend(show_main_menu(number))
        return list_data

    # Mensaje no reconocido
    data = mf.text_message("Lo siento pero no entiendo tu mensaje. Por favor, selecciona una opción del menú.", number)
    list_data.append({'data': data, 'type': False, 'needs_chatgpt': False})
    return list_data
