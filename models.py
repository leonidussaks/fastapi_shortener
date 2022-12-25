from sqlalchemy import Column, Integer, String
from database import Base

class Links(Base):
    __tablename__ = 'all_links'

    id = Column(Integer, primary_key=True,index=True)
    new_link = Column(String, nullable=False)
    reddirect_link = Column(String, nullable=False)
