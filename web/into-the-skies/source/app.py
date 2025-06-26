#!/usr/bin/env python3


import html
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlsplit

import requests
from flask import Flask, request, send_file
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app, resources={r"/generate": {"origins": "*"}})     

@app.route("/")
def spa_root():
    return app.send_static_file("index.html")


@app.errorhandler(404)
def spa_fallback(_):
    return app.send_static_file("index.html")



URL_RE   = re.compile(r"^(https?|file|gopher)://", re.I)
IMG_EXTS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".svg", ".bmp", ".tif", ".tiff", ".ico"
)


def is_image_url(url: str) -> bool:

    return urlsplit(url).path.lower().endswith(IMG_EXTS)


def tmp_html(contents: str) -> str:
    """Write contents to a temp HTML file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, "w") as f:
        f.write(contents)
    return path


def wrap_image(url: str) -> str:

    return tmp_html(
        f'<!DOCTYPE html><html><body style="margin:0">'
        f'<img src="{html.escape(url)}" style="max-width:100%"></body></html>'
    )


def wrap_iframe(url: str) -> str:
    return tmp_html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8" />
<style>html,body{{margin:0;padding:0;height:100%}}</style>
</head><body>
<iframe src="{html.escape(url)}" style="width:100%;height:100%;border:0"></iframe>
</body></html>""")



@app.route("/generate", methods=["POST"])
def generate_pdf():

    src = request.form.get("html", "").strip()
    if not src:
        return "No html/url supplied", 400

    wkhtml_input: str | None = None
    temp_files: list[str] = []


    if URL_RE.match(src):
        if is_image_url(src):

            wkhtml_input = src
        else:

            wkhtml_input = wrap_iframe(src)
            temp_files.append(wkhtml_input)

    # ---------- Handle raw HTML -------------------------------------
    else:
        wkhtml_input = tmp_html(src)
        temp_files.append(wkhtml_input)

    if wkhtml_input is None:
        return "Internal error: no input for wkhtmltopdf", 500

    pdf_path = f"/tmp/{uuid.uuid4()}.pdf"

    cmd = [
        "wkhtmltopdf",
        "--enable-local-file-access",
        "--custom-header", "User-Agent",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36",
        "--load-error-handling",       "ignore",
        "--load-media-error-handling", "ignore",
        "--javascript-delay",          "3000", 
        wkhtml_input,
        pdf_path,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        app.logger.error("wkhtmltopdf failed: %s", e.stderr.decode())
        for f in temp_files:
            os.remove(f)
        return "wkhtmltopdf error", 500

    for f in temp_files:
        os.remove(f)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"ssrf_{uuid.uuid4()}.pdf",
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
