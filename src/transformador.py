from datetime import datetime
# El nombre que usas al importar (puede ser diferente):
from bs4 import BeautifulSoup
import json
import extractor
import logging 

# En transformador.py
logger = logging.getLogger("transformador")

handler = logging.FileHandler("logs/transformador.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s — %(levelname)s — %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

def convertir_fecha(fecha: int):
    return datetime.fromtimestamp(fecha).strftime('%Y-%m-%d %H:%M:%S')

def limpiar_html(texto: str):
    if texto:
        soup = BeautifulSoup(texto, "html.parser")
        return soup.get_text()
    return None

def transformar_item(item: dict):
    logger.info(f"Transformando item con id: {item['id']}")
    return {
        "id":item['id'],
        "autor": item['by'],
        "cant_coments":item.get('descendants'),
        "calificacion":item['score'],
        "fecha": convertir_fecha(item['time']),
        "title": item['title'],
        "text": limpiar_html(item.get('text')),
        "type": item['type'],
        "url": item.get('url')
    }
    
    
def transformar(items: list):
    items_tranformados = [
        transformar_item(item) for item in items 
    ]
    return items_tranformados


def leer_crudos():
    """Intenta leer el archivo local, si no existe
    renorta una lista vacía"""
    try:
        with open("data/raw/items.json", "r", encoding="utf-8") as f:
            logger.info("Archivo items.json leído exitosamente.")
            return json.load(f)       
    except FileNotFoundError:
        logger.warning("Archivo items.json no encontrado. Se creará uno nuevo.")
        return []

def leer_limpios():
    try:
        with open("data/processed/items.json", "r", encoding="utf-8") as f:
            logger.info("Leyendo datos existentes desde data/processed/items.json")
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Archivo items.json no encontrado. Se creará uno nuevo.")
        return []
    
def guardar_limpios(items_limpios: list):
    datos = leer_limpios()
    datos.extend(items_limpios)
    with open("data/processed/items.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        logger.info(f"Archivo items.json guardado exitosamente con {len(items_limpios)} nuevos items.")
        logger.info(f"Total de items en data/processed/items.json: {len(datos)}")
    
def main():
    
    ids = extractor.obtener_ids(50)
    items = extractor.extraer(list_ids=ids, cantidad=50)
    extractor.guardar(items)
    
    datos = extractor.leer_datos()
    items_limpios = transformar(datos)
    guardar_limpios(items_limpios)

main()