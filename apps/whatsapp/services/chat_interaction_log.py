"""Registro de interacciones WhatsApp en CSV para análisis (etapa de pruebas)."""
from __future__ import annotations

import csv
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_lock = threading.Lock()

# Raíz del proyecto (…/apps/whatsapp/services -> subir 3 niveles)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_LOG_CSV = "logs/interacciones_whatsapp.csv"


def _resolved_log_path() -> Path:
    from base.load_env import load_env

    load_env()
    raw = (os.getenv("WHATSAPP_CHAT_LOG_CSV") or "").strip() or _DEFAULT_LOG_CSV
    p = Path(raw)
    if p.is_absolute():
        return p
    return _PROJECT_ROOT / p


def summarize_outgoing_whatsapp_data(data: dict[str, Any]) -> str:
    """Texto legible del payload enviado a la API de WhatsApp."""
    if not data:
        return ""
    t = data.get("type")
    if t == "text":
        return (data.get("text") or {}).get("body", "").strip()[:8000]
    if t == "interactive":
        inter = data.get("interactive") or {}
        itype = inter.get("type")
        parts: list[str] = []
        body = (inter.get("body") or {}).get("text", "")
        if body:
            parts.append(body)
        if itype == "button":
            for btn in (inter.get("action") or {}).get("buttons") or []:
                title = (btn.get("reply") or {}).get("title", "")
                if title:
                    parts.append(f"[Botón] {title}")
        elif itype == "list":
            for sec in (inter.get("action") or {}).get("sections") or []:
                for row in sec.get("rows") or []:
                    title = row.get("title", "")
                    if title:
                        parts.append(f"[Opción] {title}")
        return " ".join(parts)[:8000]
    return str(data)[:500]


def _one_line(s: str) -> str:
    if not s:
        return ""
    return " ".join(s.replace("\r", " ").splitlines()).strip()


def append_interaction(
    telefono: str,
    mensaje_usuario: str,
    uso_ia: bool,
    tema_menu: str,
    respuesta_bot: str,
) -> None:
    """Añade una fila al CSV (delimitador `;`, UTF-8 con BOM para Excel)."""
    path = _resolved_log_path()
    row = [
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        _one_line(telefono),
        "Sí" if uso_ia else "No",
        _one_line(tema_menu),
        _one_line(mensaje_usuario),
        _one_line(respuesta_bot),
    ]
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_header = not path.exists() or path.stat().st_size == 0
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            if write_header:
                w.writerow(
                    [
                        "fecha_hora",
                        "telefono",
                        "uso_ia",
                        "tema_menu",
                        "mensaje_usuario",
                        "respuesta_bot",
                    ]
                )
            w.writerow(row)


def get_log_path() -> Path:
    return _resolved_log_path()
