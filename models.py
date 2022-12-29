from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///links.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()


class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    old_link = Column(String)
    new_link = Column(String)
    data_created = Column()


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    admin = Column(Boolean)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
