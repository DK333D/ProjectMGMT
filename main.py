
from datetime import datetime
from typing import Annotated

from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

import moje_projekty_widok_handle
import projekty_handle
import stanowiska_handle
import role_handle
import tablice_handle
import osoby_handle
import zadania_handle
import zadania_relacja_typy_handle
import zadania_relacje_handle
import projekt_osoba_rola_handle
import projekt_info_handle
import zarejestruj_handle
import zaloguj_handle
import administratorzy_handle

import help
import logging

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Mounting the directory containing CSS and other static files
app.mount("/static", StaticFiles(directory="templates"), name="static")
app.mount("/imgs", StaticFiles(directory="imgs"), name='images')

# Create a logger instance
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=help.SECRET_KEY)


@app.get("/a", response_class=HTMLResponse)
def serve():
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
        <img src="imgs/kotek.png">
        <h1>Hello World</h1>
        </body>
    </html>
    """

@app.get('/')
def increment(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "ile": None})


@app.get('/dashboard')
def increment(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "session_data": request.session.get('email')})

@app.post('/')
def increment(request: Request, ile: Annotated[int, Form()]):
    if ile > 100:
        ile = 100
    if ile < 0:
        ile = 0
    return templates.TemplateResponse("form.html", {"request": request, "ile": ile})

app.include_router(projekty_handle.router)
app.include_router(stanowiska_handle.router)
app.include_router(role_handle.router)
app.include_router(tablice_handle.router)
app.include_router(osoby_handle.router)
app.include_router(zadania_handle.router)
app.include_router(zadania_relacja_typy_handle.router)
app.include_router(zadania_relacje_handle.router)
app.include_router(projekt_osoba_rola_handle.router)
app.include_router(projekt_info_handle.router)
app.include_router(zaloguj_handle.router)
app.include_router(zarejestruj_handle.router)
app.include_router(moje_projekty_widok_handle.router)
app.include_router(administratorzy_handle.router)
