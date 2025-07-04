# Inicia el servidor de backend:

    uvicorn backend:app --reload

# URL a la web app de prueba de Azure, utilizada como URL de devolución de llamada del Webhook

https://test-humanidades-wa.azurewebsites.net/bot_whatsapp/whatsapp

# URL a la web app de prueba local, utilizada como URL de devolución de llamada del Webhook

https://clearly-prime-eel.ngrok-free.app/bot_whatsapp/whatsapp

# Correr el servidor de Ngrok en local, para disponer la app en internet con dominio propio(de prueba) y SSL

ngrok http --url=clearly-prime-eel.ngrok-free.app 8000

# Para desplegar en Azure hacer los siguientes cambios:

---

Esto es necesario porque el servidor Azure es en GNU/Linux y tiene la versión de Python (3.10)
que tiene problemas con la versión de la librería de Chroma.

- En la web app de Azure, tener seteado las siguientes secciones del menú:

  - variables de entorno
    SCM_DO_BUILD_DURING_DEPLOYMENT = true
  - configuración -> comando de inicio
    gunicorn -k uvicorn.workers.UvicornWorker backend:app

- Descomentar en requirements.txt la linea de:
  pysqlite3-binary

- Descomentar en ia/embeddings/manage_embeddings.py las siguientes líneas(son las primeras):
  **import**('pysqlite3')
  import sys
  sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Para generar los distintos archivos con el scraper hay que pasar los valores en el body:

---

Método: POST
URL: 127.0.0.1:8000/scraper/generate_pd
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
