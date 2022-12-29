import string
from random import choice

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse as Redir
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from starlette.responses import HTMLResponse

from models import db, Links

###
domain_name = "https://b794-2-57-83-73.eu.ngrok.io/"
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
    # {domain_name}/
    new_link = random_string()
    old_link = f'https://{main_link}'
    linker = Links(new_link=new_link, old_link=old_link)
    db.add(linker)
    db.commit()
    # return {"short_link": domain_name+new_link, "main_link": old_link, "status": "success"}
    # request.headers.values()[0] +
    return templates.TemplateResponse("index.html", context={"request": request, "new_link": new_link})


@app.get('/{url}')
async def redir(url: str):
    print("лох")
    try:
        x = db.execute(select(Links).filter_by(new_link=url)).scalar_one()
        return Redir(x.old_link)
    except NoResultFound:
        return {"status": "not found link!"}
        # return templates.TemplateResponse("index.html", context={"request": request})


def random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for _ in range(6))
    return result_str
