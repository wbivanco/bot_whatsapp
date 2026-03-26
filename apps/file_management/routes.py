import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from base.load_env import load_env
from base.sessions import require_session

from apps.chatbot.routes import create_embeddings
from ia.embeddings.manage_embeddings import EmbeddingsManager

router = APIRouter()

load_env()
upload_directory = os.getenv("PATH_TO_UPLOAD_FOLDER")
api_key = os.getenv("OPENAI_API_KEY")
persist_directory = os.getenv("PERSIST_CHROMADB_FOLDER")

templates = Jinja2Templates(directory=["shared_templates", "apps/backoffice/templates", "apps/file_management/templates", "apps/chatbot/templates"])


def _list_visible_upload_files(directory: str) -> list:
    """Nombres de archivo para el panel: sin metadatos de Git (.gitkeep) ni otros ocultos."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        f
        for f in os.listdir(directory)
        if not f.startswith(".")
    )


@router.get("/list_files", response_class=HTMLResponse)
async def list_files(request: Request): 
    """ Listar los archivos que formaran parte de la base de conocimiento."""
    # Verifico si el usuario tiene una sesión activa
    response = require_session(request)
    if isinstance(response, RedirectResponse):
        return response 
    
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory, exist_ok=True)        
    files = _list_visible_upload_files(upload_directory)
    message = request.session.pop("message", None)
    return templates.TemplateResponse("admin_files.html", {"request": request, "files": files, "message": message})

@router.post("/delete/")
def delete_file(request: Request, filename: str = Form(...)):  
    """Elimina el archivo en disco y los vectores asociados en Chroma (metadato source)."""
    safe_name = os.path.basename(filename)
    file_path = os.path.join(upload_directory, safe_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        try:
            manager = EmbeddingsManager("openai", api_key, persist_directory)
            removed = manager.delete_vectors_for_source(safe_name)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Archivo eliminado pero falló la actualización de la BD vectorial: {e}",
            ) from e
        if removed:
            extra = f"Se quitaron {removed} fragmento(s) de la base vectorial."
        else:
            extra = (
                "No se encontraron vectores con ese nombre en Chroma "
                "(p. ej. el archivo no estaba indexado o el metadato source no coincide)."
            )
        request.session["message"] = f"Archivo '{safe_name}' eliminado. {extra}"
        return RedirectResponse("/files/list_files", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

@router.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    """ Sube un archivo a la base de conocimiento y actualiza embeddings."""
    try:
        file_path = os.path.join(upload_directory, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        create_embeddings()
        request.session["message"] = f"Archivo: '{file.filename}' subido exitosamente. Actualización correcta de la base de conocimiento."
        return RedirectResponse("/files/list_files", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   