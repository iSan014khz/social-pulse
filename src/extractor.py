from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import os
import requests
import json
import logging

logger = logging.getLogger("extractor")

handler = logging.FileHandler("logs/extractor.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s — %(levelname)s — %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

load_dotenv()

app_name = os.getenv("APP_NAME")
api = os.getenv("HN_BASE_URL")
end_point = os.getenv("HN_TOP_STORIES")
item = os.getenv("HN_ITEM")
max_post = os.getenv("MAX_POSTS")

def obtener_ids(cant_items: int) -> list:
    """Recibe los posts mas virales y 
    nos quedamos con n cantidad"""
    
    response = requests.get(f"{api}{end_point}").json()
    logger.info(f"Se obtuvieron {cant_items} ids: {response[:cant_items]}")
    return response[:cant_items]

def obtener_item(id: int) -> json:
    """Recibe el id del post y retorna su infromación"""
    
    try:
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty").json()
        logger.info(f"Información obtenida del post con id: {id}")
        if response is None:
            logger.warning(f"Item {id} no existe o fue eliminado.")
            return None
        return response
    
    except requests.RequestException as e:
        logger.error(f"Error al obtener información del post con id: {id}. Error: {e}")
        return None
    
def extraer(list_ids: list, cantidad: int) -> list:
    """Hace 10 gets por seg y de cada id recibe la
    información del post"""
    logger.info(f"Extrayendo información de posts: {list_ids[:cantidad]}...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        items = list(executor.map(obtener_item, list_ids[:cantidad]))
        logger.info(f"Información de posts:{list_ids[:cantidad]} extraída exitosamente.")
    return items

def leer_datos():
    """Intenta leer el archivo local, si no existe
    renorta una lista vacía"""
    try:
        with open("data/raw/items.json", "r", encoding="utf-8") as f:
            logger.info("Archivo items.json leído exitosamente.")
            return json.load(f)       
    except FileNotFoundError:
        logger.warning("Archivo items.json no encontrado. Se creará uno nuevo.")
        return []
    
def guardar(items: list):
    datos = leer_datos()
    datos.extend(items)
    with open("data/raw/items.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(datos, indent=2))
        logger.info(f"Items guardados exitosamente en items.json. \nTotal de items: {len(datos)}.")
        
def main():
    ids = obtener_ids(10)
    items = extraer(list_ids=ids, cantidad=10)
    guardar(items)

main()

# Lecciones:
"""Se usan en diferentes ocasiones"""
#json.loads(f)  # ❌ f es un archivo, no un string
#json.load(f)   # ✅ f es un archivo