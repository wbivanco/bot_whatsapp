def text_message(text, number):
    """ Formatea la data para un mensaje de texto. """
    data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": text
            }
        }
    
    return data

def text_format_message(number, text):
    """ Formatea la data para un mensaje de texto con formato, ejemplos(negrita, cursiva, tachado, código):
    formatted_text = f"*{text}* - _{text}_ - ~{text}~ - ```{text}```"
    """
    formatted_text = f"*{text}*"
    data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": formatted_text
            }
        }
    
    return data

def image_message(number, link):
    """ Formatea la data para un mensaje con imagen, ejemplo de link:
    "https://botwhatsappsample.blob.core.windows.net/images/minion.jpg"
    """
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "image",
            "image": {
                "link": link
            }
        }
    
    return data

def audio_message(number, link):
    """ Formatea la data para un mensaje con audio, ejemplo de link:
    "https://botwhatsappsample.blob.core.windows.net/images/minion.mp3"
    """
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "audio",
            "audio": {
                "link": link
            }
        }

    return data

def video_message(number, link):
    """ Formatea la data para un mensaje con video, ejemplo de link:
    "https://botwhatsappsample.blob.core.windows.net/images/minion.mp4"
    """
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "video",
            "video": {
                "link": link
            }
        }

    return data

def document_message(number, link):
    """ Formatea la data para un mensaje con documento, ejemplo de link:
    "https://botwhatsappsample.blob.core.windows.net/images/minion.pdf"
    """
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "document",
            "document": {
                "link": link
            }
        }

    return data

def location_message(number, location):
    """ Formatea la data para un mensaje con ubicación, ejemplo de la data:
    location = {
        "latitude": "-28.452925850805755",
        "longitude": "-65.7575180790931",
        "name": "Casa",
        "address": "Av Recalde 2120"
    }
    """
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "location",
            "location": {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "name": location["name"],
                "address": location["address"]
            }
        }

    return data

def buttons_message(number, text, buttons):
    """ Formatea la data para un mensaje con botones y con emojis tanto para el text como para los titles. 
    buttons es una array de titulos de botones. """
    formatted_buttons = []
    for idx, button in enumerate(buttons, start=1):
        formatted_button = {
            "type": "reply",
            "reply": {
                "id": f"{idx:03}",
                "title": button
            }
        }
        formatted_buttons.append(formatted_button)

    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": text
                },
                "action": {
                    "buttons": formatted_buttons
                }
            }
        }

    return data

def list_message(number, sections):
    """ Formatea la data para un mensaje con listas, tambien se puede usar emojis.
    Tener en cuenta que sections es un array de diccionarios, cada diccionario representa
     una seccion y contiene una lista de filas; tiene la siguiente estructura:
    sections = [
        {
            "title": "Buy and sell products",
            "rows": [
                {
                    "id": "main-buy",
                    "title": "Comprar",
                    "description": "Buy the best product for your home"
                },
                {
                    "id": "main-sell",
                    "title": "Vender",
                    "description": "Sell your products"
                }
            ]
        },
        {
            "title": "📍center of attention",
            "rows": [
                {
                    "id": "main-agency",
                    "title": "Agencia",
                    "description": "You can visit our agency"
                },
                {
                    "id": "main-contact",
                    "title": "Centro de Contacto",
                    "description": "One of our agents will assist you"
                }
            ]
        }
    ]
    """
    formatted_sections = []
    for section in sections:
        formatted_section = {
            "title": section["title"],
            "rows": []
        }
        for row in section["rows"]:
            formatted_row = {
                "id": row["id"],
                "title": row["title"] 
            }
            formatted_section["rows"].append(formatted_row)
        formatted_sections.append(formatted_section)

    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "✅ Tengo estas opciones para ti:"
                },
                "footer": {
                    "text": "Selecciona una opción de la lista"
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": formatted_sections
                }
            }
        }

    return data