import datetime
import uuid
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse as Redir
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from starlette.responses import HTMLResponse

from models import db, Links

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/all")
async def all_links():
    x = db.query(Links).all()
    return x


@app.post("/link")
async def short_link(request: Request, main_link=Form()):
    new_link = random_string()
    linker = Links(new_link=new_link, old_link=main_link, date_created=datetime.datetime.now())
    db.add(linker)
    db.commit()
    return templates.TemplateResponse("index.html", context={"request": request, "new_link": new_link})


@app.get('/404')
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", context={"request": request})


@app.get('/{url}')
async def redir(url: str):
    try:
        x = db.execute(select(Links).filter_by(new_link=url)).scalar_one()
        protocol = urlparse(x.old_link)
        if protocol.scheme == '':
            return Redir("https://" + x.old_link, status_code=302)
        return Redir(x.old_link, status_code=302)
    except NoResultFound:
        return Redir('/404')


def random_string():
    return uuid.uuid4().hex[:6].lower()
