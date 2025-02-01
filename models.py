from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Projects(Base):
    __tablename__='projects'
    id=Column(Integer,primary_key=True)
    Title=Column(String(255),nullable=False)
    Description=Column(String(500),nullable=False)
    Category=Column(String(255),nullable=True)
    project_link=Column(String(255),nullable=True)
    image_filename = Column(String(500), nullable=False)