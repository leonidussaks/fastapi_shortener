import string
from random import choice

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse as Redir
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.responses import HTMLResponse

SQLALCHEMY_DATABASE_URL = "sqlite:///./links.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
###
domain_name = "https://b794-2-57-83-73.eu.ngrok.io/"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
SQLALCHEMY_DATABASE_URL = "sqlite:///links.db"


class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    old_link = Column(String)
    new_link = Column(String)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


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
    old_link = main_link
    linker = Links(new_link=new_link, old_link=old_link)
    db.add(linker)
    db.commit()
    # return {"short_link": domain_name+new_link, "main_link": old_link, "status": "success"}
    return templates.TemplateResponse("index.html", context={"request": request, "new_link": domain_name + new_link})


@app.get('/{url}')
async def redir(url: str):
    try:
        x = db.execute(select(Links).filter_by(new_link=url)).scalar_one()
        return Redir(x.old_link)
    except NoResultFound:
        return {"status": "not found link!"}


def random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for _ in range(6))
    return result_str
