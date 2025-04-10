import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from base.load_env import load_env
from apps.chatbot.routes import router as chatbot_router
from apps.file_management.routes import router as file_management_router
from apps.whatsapp.routes import router as whatsapp_router
from apps.scraper.routes import router as scraper_router
from apps.login.routes import router as login_router
from apps.backoffice.routes import router as backoffice_router

load_env()
openai_api_key = os.getenv("OPENAI_API_KEY")
persist_directory = os.getenv("PERSIST_CHROMADB_FOLDER")
upload_directory = os.getenv("PATH_TO_UPLOAD_FOLDER")

app = FastAPI(
    title="HumaBot API",
    description="API para el bot de Whatsapp de la Facultad de Humanidades",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(SessionMiddleware, secret_key="ijdjandsncl as23nff m,")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URL en desarrollo; ajusta para producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.mount("/login_static", StaticFiles(directory="apps/login/static"), name="login_static")
app.mount("/backoffice_static", StaticFiles(directory="apps/backoffice/static"), name="backoffice_static")
app.mount("/files_static", StaticFiles(directory="apps/file_management/static"), name="files_static")
app.mount("/chatbot_static", StaticFiles(directory="apps/chatbot/static"), name="chatbot_static")

# Configuración de plantillas Jinja2, si se modifica aquí, se debe modificar en todos los routes
templates = Jinja2Templates(directory=[
    "shared_templates", 
    "apps/backoffice/templates", 
    "apps/file_management/templates", 
    "apps/chatbot/templates"
    ])

@app.get("/", tags=["Redirection to login"])
async def root():
    return RedirectResponse(url="/auth/login")

# Incluir routers
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(file_management_router, prefix="/files", tags=["File Management"])
app.include_router(whatsapp_router, prefix="/bot_whatsapp", tags=["WhatsApp Bot"])
app.include_router(scraper_router, prefix="/scraper", tags=["Scraper"])
app.include_router(login_router, prefix="/auth", tags=["Login"])
app.include_router(backoffice_router, prefix="/backoffice", tags=["Backoffice"])

