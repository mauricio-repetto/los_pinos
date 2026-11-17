#!/usr/bin/env python3
"""Descarga desde Google Drive los archivos livianos de este repo (notebooks,
slides en PDF y scripts auxiliares) según `drive_assets.json`.

Los archivos pesados (pesos de modelos, checkpoints, datasets, videos) NO se
descargan: están listados en el README con su link a Drive.

Uso (desde la raíz del repo):
    python scripts/fetch_assets.py            # descarga lo que falte
    python scripts/fetch_assets.py --force    # vuelve a descargar todo

Solo usa la librería estándar de Python (3.8+).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "drive_assets.json"

URLS = {
    # Google Slides exportado a PDF
    "slides": "https://docs.google.com/presentation/d/{id}/export/pdf",
    # Cualquier archivo binario/texto guardado en Drive (.ipynb, .py, .csv, ...)
    "file": "https://drive.usercontent.google.com/download?id={id}&export=download&confirm=t",
}

USER_AGENT = "Mozilla/5.0 (fetch_assets.py)"
WARN_MB = 50  # GitHub avisa a partir de 50 MB y rechaza archivos > 100 MB


def validate(kind: str, dest: Path, data: bytes) -> None:
    head = data[:512].lstrip().lower()
    if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
        raise ValueError(
            "Drive devolvió una página HTML en lugar del archivo "
            "(¿el archivo no es público o pide confirmación/login?)"
        )
    if kind == "slides" and not data.startswith(b"%PDF"):
        raise ValueError("la exportación no parece ser un PDF válido")
    if dest.suffix == ".ipynb":
        nb = json.loads(data.decode("utf-8"))
        if "cells" not in nb:
            raise ValueError("el .ipynb no tiene la clave 'cells'")


def download(kind: str, file_id: str) -> bytes:
    url = URLS[kind].format(id=file_id)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="re-descargar aunque el archivo exista")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = manifest.get("download", [])
    print(f"[{manifest.get('repo', REPO_ROOT.name)}] {len(items)} archivo(s) a sincronizar desde Drive")

    failures = 0
    for item in items:
        dest = REPO_ROOT / item["dest"]
        kind = item["kind"]
        if dest.exists() and not args.force:
            print(f"  = {item['dest']} (ya existe, se omite)")
            continue
        try:
            data = download(kind, item["id"])
            validate(kind, dest, data)
        except Exception as exc:  # noqa: BLE001 - queremos seguir con el resto
            failures += 1
            print(f"  ! {item['dest']}: ERROR -> {exc}", file=sys.stderr)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as tmp:
            tmp.write(data)
        Path(tmp.name).replace(dest)
        size_mb = len(data) / 1_048_576
        flag = "  <-- ojo: archivo grande para git" if size_mb > WARN_MB else ""
        print(f"  + {item['dest']} ({size_mb:.1f} MB){flag}")

    if failures:
        print(f"{failures} descarga(s) fallaron; revisá los mensajes de arriba.", file=sys.stderr)
        return 1
    print("Listo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
