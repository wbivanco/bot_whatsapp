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

Ejemplo: ngrok http --url=clearly-prime-eel.ngrok-free.app 8000

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
3.  Cuando pregunte "run build commands on target server": responder NO.

------------------------------------------------------------------------

🚀 CI/CD con GitHub Actions (Despliegue Automático)

El proyecto incluye un workflow de GitHub Actions que despliega automáticamente a Azure cuando se hace push a la rama `main`.

**Configuración inicial (solo una vez):**

1. **Obtener el Publish Profile:**
   - En Azure Portal, ve a tu App Service → Overview
   - Haz clic en "Get publish profile" (Obtener perfil de publicación)
   - Se descargará un archivo `.PublishSettings`

2. **Configurar el Secret en GitHub:**
   - Ve a: `https://github.com/wbivanco/bot_whatsapp/settings/secrets/actions`
   - Haz clic en "New repository secret"
   - **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Secret:** Abre el archivo `.PublishSettings` descargado y copia TODO su contenido (desde `<publishData>` hasta `</publishData>`)
   - Haz clic en "Add secret"

3. **Probar el despliegue:**
   - Haz un commit y push a `main` → se desplegará automáticamente
   - O ejecuta manualmente: Actions → "Deploy to Azure App Service" → Run workflow

**Nota:** El workflow despliega todo el código incluyendo documentos y BD vectorial, manteniendo la integridad referencial.

**Archivo de configuración:** `.github/workflows/azure-deploy.yml`

------------------------------------------------------------------------

Verificación en Kudu: ls -l /home/site/wwwroot

Debe aparecer backend.py, requirements.txt, apps/, ia/, db/, files/,
etc.

Probar: https://TU-APP.azurewebsites.net/docs

------------------------------------------------------------------------

📥 Descargar documentos desde Azure

**Opción 1: Kudu (Más fácil)**
1. Ve a: `https://TU-APP.scm.azurewebsites.net`
2. O desde Azure Portal: App Service → "Advanced Tools" → "Go"
3. Navega a `site/wwwroot/files/uploads/` y `site/wwwroot/db/dbchroma/`
4. Selecciona y descarga los archivos

**Opción 2: SSH desde Azure Portal**
1. App Service → "SSH" o "Herramientas de desarrollo" → "SSH"
2. Ejecuta: `cd /home/site/wwwroot && ls -la files/uploads/ db/dbchroma/`
3. Usa Kudu para descargar los archivos

------------------------------------------------------------------------

📁 Ubicación de los documentos

Los documentos se guardan en las siguientes carpetas (relativas a la raíz del proyecto):

1. Archivos subidos manualmente (PDFs, DOCX, TXT):
   - Local: `files/uploads/`
   - Azure: `/home/site/wwwroot/files/uploads/`
   - Variable de entorno: `PATH_TO_UPLOAD_FOLDER = 'files/uploads'`

2. PDFs generados por el scraper:
   - Local: `files/uploads/` (mismo directorio que los archivos subidos)
   - Azure: `/home/site/wwwroot/files/uploads/`

3. Base de datos de embeddings (Chroma):
   - Local: `db/dbchroma/`
   - Azure: `/home/site/wwwroot/db/dbchroma/`
   - Variable de entorno: `PERSIST_CHROMADB_FOLDER = 'db/dbchroma'`

**Nota importante sobre el repositorio:**
- Los documentos en `files/uploads/` **SÍ se suben al repositorio** para mantener integridad referencial
- La base de datos de embeddings (`db/dbchroma/`) **TAMBIÉN se sube** al repositorio para mantener integridad completa
- Cada cambio en `files/uploads/` actualiza automáticamente la BD vectorial mediante el CRUD de administración
- Ambos deben estar sincronizados en el repositorio para mantener la integridad referencial

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