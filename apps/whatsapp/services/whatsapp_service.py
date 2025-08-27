import requests
import json

def send_message_whatsapp(data, token, url):
    """ Recibe la data y envia el mensaje por whatsapp. """
    try:
        token = token
        api_url = url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        
        # Debug: imprimir el mensaje que se está enviando
        print("Enviando mensaje:", json.dumps(data, indent=2))
        
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        # Debug: imprimir la respuesta
        print("Respuesta de WhatsApp:", response.status_code, response.text)
        
        if response.status_code == 200:
            return True
        
        return False
    except requests.exceptions.RequestException as exception:
        print("Error en la petición:", str(exception))
        return False
    