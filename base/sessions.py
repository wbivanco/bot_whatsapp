from fastapi import Request
from fastapi.responses import RedirectResponse

def require_session(request: Request):
    """Verifica si el usuario tiene una sesión iniciada."""
    if not request.session.get("username"):
        return RedirectResponse(url="/auth/login")