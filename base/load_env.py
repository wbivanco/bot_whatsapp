import ast
import os
from pathlib import Path


def _normalize_files_types_env() -> None:
    """Acepta FILES_TYPES como .pdf,.docx o como lista estilo Python en el .env."""
    raw = (os.environ.get("FILES_TYPES") or ".pdf,.docx,.txt").strip()
    if not raw:
        os.environ["FILES_TYPES"] = ".pdf,.docx,.txt"
        return
    if raw.startswith("["):
        try:
            parsed = ast.literal_eval(raw)
            if isinstance(parsed, list):
                os.environ["FILES_TYPES"] = ",".join(str(x).strip() for x in parsed if str(x).strip())
                return
        except (ValueError, SyntaxError):
            pass
    os.environ["FILES_TYPES"] = raw


def load_env():
    """Carga el .env y normaliza rutas de proyecto relativas a absolutas (raíz del repo)."""
    from dotenv import load_dotenv

    load_dotenv()
    root = Path(__file__).resolve().parent.parent
    for key in ("PERSIST_CHROMADB_FOLDER", "PATH_TO_UPLOAD_FOLDER"):
        val = os.environ.get(key)
        if not val:
            continue
        p = Path(val)
        if not p.is_absolute():
            os.environ[key] = str((root / val).resolve())

    _normalize_files_types_env()