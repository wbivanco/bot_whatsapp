import requests
import json

def send_message_whatsapp(data, token, url):
    """ Recibe la data y envia el mensaje por whatsapp. """
    try:
        token = token
        api_url = url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            return True
        
        return False
    except Exception as exception:
        print(exception)
        return False
