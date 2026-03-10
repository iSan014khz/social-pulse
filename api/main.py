import sys
sys.path.append("src")

from sqlalchemy import desc, func
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Autor, Post
from datetime import datetime


engine = create_engine("sqlite:///data/social_pulse.db")
Base.metadata.create_all(engine)

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {
        "Bienvenido!": datetime.now(),
    }

@app.get("/post/top10")
def top10_post():
    with Session(engine) as session:
        top10_post = session.query(Post).order_by(desc(Post.calificacion)).limit(10).all()
    return {
        "top 10 post": [
            {
                "id":p.id, 
                "titulo": p.title,
                "calificación": p.calificacion
            } for p in top10_post
        ]
    }
    
@app.get("/post/top_coments")
def top_coments():
    with Session(engine) as session:
        top_coments = session.query(Post).order_by(desc(Post.cant_coments)).limit(10).all()
    return {
        "top 10 post": [
            {
                "id":p.id, 
                "titulo": p.title,
                "cant_comentarios": p.cant_coments
            } for p in top_coments
        ]
    }
    
@app.get("/actividad/horas")
def horas_activas():
    with Session(engine) as session:
        #func.strftime() no es un método predefinido
        # pero funciona en tiempo de ejecución
        horas = session.query(func.strftime("%H", Post.fecha).label("Horas"),
                              func.count().label("Cantidad_Posts"))\
            .order_by("Horas")\
            .group_by("Horas")\
            .limit(24).all()

    return {
        "Horas":[
            {
                "Hora":hora,
                "Cantidad_de_Posts": num_post
            } for hora, num_post in horas
        ]
    }
    
@app.get("/autores/top")
def top_autores():
    with Session(engine) as session:
        autores = session.query(Autor.nombre, func.count(Post.id_autor).label("cantidad_posts"))\
        .join(Autor, Post.id_autor == Autor.id)\
        .group_by(Autor.id)\
        .order_by(desc("cantidad_posts"))\
        .limit(10).all()
        
    return {
        "Top":[
            {
                "autor": nombre,
                "cantidad_posts": cantidad
            } for nombre, cantidad in autores
        ]
    }