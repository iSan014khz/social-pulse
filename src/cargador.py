from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Autor, Post
import json
import logging

logger = logging.getLogger("cargador")
# agrega tus handlers aquí igual que en los otros módulos
handler = logging.FileHandler("logs/cargador.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s — %(levelname)s — %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

engine = create_engine("sqlite:///data/social_pulse.db")
Base.metadata.create_all(engine)

def leer_datos():
    try:
        with open("data/processed/items.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def cargar(items: list):
    with Session(engine) as session:
        for item in items:

            # Se busca si ya existe un autor con ese nombre 
            autor = session.query(Autor).filter_by(nombre=item['autor']).first()
            
            if not autor:
                autor = Autor(nombre=item['autor'])
                session.add(autor)
                session.commit()
                logger.info(f"Se ha cargado exitosamente: {autor.nombre}.")
            else:
                logger.warning(f"Autor: '{autor.nombre}' no se cargó porqué ya existe.")

            post_existente = session.query(Post).filter_by(id=item['id']).first()
            
            if not post_existente:
                post = Post(
                id_autor=autor.id,
                id=item['id'],
                cant_coments=item['cant_coments'],
                calificacion=item['calificacion'],
                fecha=item['fecha'],
                title=item['title'],
                text=item['text'],
                type=item['type'],
                url=item['url']
                )
                session.add(post)
                session.commit()
                logger.info(f"Se ha cargado exitosamente el post: {post.id}")
            else:
                logger.warning(f"Post {item['id']} ya existe, se omite.")
            

def main():
    data = leer_datos()
    cargar(items=data)

main()