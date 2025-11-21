Proyecto Backend – Webhooks WhatsApp + Scraper + Embeddings IA

Este proyecto implementa: - Un backend FastAPI. - Webhook para WhatsApp
Cloud API. - Scraper para generar archivos automáticos. - Módulos de
embeddings y vectorización. - Despliegue en Azure Web App (Python
3.10). - Exposición local mediante Ngrok.

------------------------------------------------------------------------

🚀 Desarrollo local

Iniciar el servidor FastAPI en local: uvicorn backend:app –reload

Documentación local: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

🌐 Exponer en Internet mediante Ngrok (modo pruebas)

    ngrok http --url=TU-URL.ngrok-free.app 8000

Ejemplo: ngrok http –url=clearly-prime-eel.ngrok-free.app 8000

Webhook local:
https://clearly-prime-eel.ngrok-free.app/bot_whatsapp/whatsapp

------------------------------------------------------------------------

☁️ Webhook en Azure (producción)
https://test-humanidades-wa.azurewebsites.net/bot_whatsapp/whatsapp

------------------------------------------------------------------------

🟦 Despliegue en Azure – INSTRUCCIONES CORRECTAS

Eliminar las siguientes variables si existen:

SCM_DO_BUILD_DURING_DEPLOYMENT 
SCM_RUN_FROM_PACKAGE
WEBSITE_RUN_FROM_PACKAGE 
WEBSITE_RUN_FROM_ZIP

Startup Command: python -m uvicorn backend:app –host 0.0.0.0 –port 8000

------------------------------------------------------------------------

Compatibilidad Python 3.10 + Chroma

En requirements.txt descomentar: pysqlite3-binary

En ia/embeddings/manage_embeddings.py descomentar: 
import pysqlite3
import sys 
sys.modules[‘sqlite3’] = sys.modules.pop(‘pysqlite3’)

------------------------------------------------------------------------

Desplegar desde VS Code:

1.  Abrir carpeta raíz del proyecto.
2.  Deploy to Web App.
3.  Cuando pregunte “run build commands on target server”: responder NO.

------------------------------------------------------------------------

Verificación en Kudu: ls -l /home/site/wwwroot

Debe aparecer backend.py, requirements.txt, apps/, ia/, db/, files/,
etc.

Probar: https://TU-APP.azurewebsites.net/docs

------------------------------------------------------------------------
# Para generar los distintos archivos con el scraper hay que pasar los valores en el body:
🛠️ Endpoint del Scraper

POST → http://127.0.0.1:8000/scraper/generate_pd

BODY(raw):
{
"files": [
{
"filename": "Grado",
"title": "Facultad de Humanidades - UNCa",
"subtitle": "Oferta Académica de Grado",
"url": "https://huma.unca.edu.ar/oferta-academica/grado"
},
{
"filename": "Posgrado",
"title": "Facultad de Humanidades - UNCa",
"subtitle": "Oferta Académica de Posgrado",
"url": "https://huma.unca.edu.ar/oferta-academica/posgrado"
},
{
"filename": "Diplomaturas",
"title": "Facultad de Humanidades - UNCa",
"subtitle": "Oferta Académica de Diplomaturas",
"url": "https://huma.unca.edu.ar/oferta-academica/diplomaturas"
}
 ]
}

------------------------------------------------------------------------
# Video donde muestra como hacer para registrar el número de teléfono 
🎥 Video útil: https://www.youtube.com/watch?v=4eUwiK1C4JI

------------------------------------------------------------------------

Autor: Proyecto backend para la Facultad de Humanidades – UNCa
Desarrollado por Walter Bivanco (Inapsis)