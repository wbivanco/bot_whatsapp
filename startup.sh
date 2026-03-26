#!/usr/bin/env bash
# Arranque en Azure App Service: descomprime Chroma si el CI subió un único .tgz
# (evita fallos de rsync paralelo de Kudu con data_level0.bin y archivos hermanos).
set -euo pipefail
cd /home/site/wwwroot

CHROMA_TGZ="db/dbchroma/chroma_vector_store.tgz"
if [ -f "$CHROMA_TGZ" ]; then
  echo "[startup] Extrayendo Chroma desde $CHROMA_TGZ ..."
  tar -xzf "$CHROMA_TGZ" -C db/dbchroma
  rm -f "$CHROMA_TGZ"
  echo "[startup] Chroma listo."
fi

exec python -m uvicorn backend:app --host 0.0.0.0 --port 8000
