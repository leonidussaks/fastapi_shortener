from random import choice

from fastapi import FastAPI
from fastapi.responses import RedirectResponse as Redir, HTMLResponse as Html

import string

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./links.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
###
domain_name = "http://127.0.0.1:8000"
app = FastAPI()
SQLALCHEMY_DATABASE_URL = "sqlite:///links.db"


class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    old_link = Column(String)
    new_link = Column(String)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


@app.get("/")
async def root():
    Html('index.html')


@app.get("/link/{link}")
async def linker(link: str):
    #{domain_name}/
    new_link = random_string()
    old_link = f'https://{link}'
    linker = Links(new_link=new_link, old_link=old_link)
    db.add(linker)
    db.commit()
    return {"short_link": new_link, "main_link": old_link, "status": "success"}

# create database for linkds

@app.get('/test')
async def test():
    responce = Redir(url='https://vk.com')
    return responce
# todo: fix this shit
@app.get('/{url}')
async def redir(url: str):
    x = db.query(Links.new_link).all()
    for fuck in x:
        if url == fuck[0]:
            print("я ебланище")
            print(db.query(Links.new_link).get(Links.old_link))
        print(fuck[0])

def random_string():
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for _ in range(6))
    return result_str
