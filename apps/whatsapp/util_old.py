def get_text_user(message):
    """ Verifica el tipo de mensaje que se recibe y retorna el texto. """

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
            print("sin mensaje")
            
    else:
        print("sin mensaje")

    return text


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


def text_format_message(number):
    """ Formatea la data para un mensaje de texto con formato. """

    data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": "*Hola usuario* - _Hola usuario_ - ~Hola usuario~ - ```Hola usuario```"
            }
        }
    
    return data


def image_message(number):
    """ Formatea la data para un mensaje con imagen. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "image",
            "image": {
                "link": "https://botwhatsappsample.blob.core.windows.net/images/minion.jpg"
            }
        }
    
    return data


def audio_message(number):
    """ Formatea la data para un mensaje con audio. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "audio",
            "audio": {
                "link": "https://botwhatsappsample.blob.core.windows.net/images/minion.mp3"
            }
        }

    return data


def video_message(number):
    """ Formatea la data para un mensaje con video. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "video",
            "video": {
                "link": "https://botwhatsappsample.blob.core.windows.net/images/minion.mp4"
            }
        }

    return data


def document_message(number):
    """ Formatea la data para un mensaje con documento. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "document",
            "document": {
                "link": "https://botwhatsappsample.blob.core.windows.net/images/minion.pdf"
            }
        }

    return data


def location_message(number):
    """ Formatea la data para un mensaje con ubicación. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "location",
            "location": {
                "latitude": "-28.452925850805755",
                "longitude": "-65.7575180790931",
                "name": "Casa",
                "address": "Av Recalde 2120"
            }
        }

    return data


def buttons_message(number):
    """ Formatea la data para un mensaje con botones. """
    
    data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": "¿Confirmas tu registro?"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "001",
                                "title": "✅Ingresar"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "002",
                                "title": "❌Registrarse"
                            }
                        }
                    ]
                }
            }
        }

    return data


def list_message(number):
    """ Formatea la data para un mensaje con listas. """
    
    data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "✅ Tengo estas opciones"
                },
                "footer": {
                    "text": "Seleccione una opción"
                },
                "action": {
                    "button": "Ver optiones",
                    "sections": [
                        {
                            "title": "Buy and sell products",
                            "rows": [
                                {
                                    "id": "main-buy",
                                    "title": "Comprar",
                                    "description": "Buy the best product your home"
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
                                    "description": "Your can visit our agency"
                                },
                                {
                                    "id": "main-contact",
                                    "title": "Centro de Contacto",
                                    "description": "One of our agents will assist you"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    return data