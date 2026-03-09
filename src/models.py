from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Autor(Base):
    __tablename__ = "autores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    id_autor = Column(Integer, ForeignKey("autores.id"))
    cant_coments = Column(Integer)
    calificacion = Column(Integer)
    fecha = Column(String)
    title = Column(String)
    text = Column(Text)
    type = Column(String)
    url = Column(String)