from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import os
import requests
import json

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
    return response[:cant_items]

def obtener_item(id: int) -> json:
    """Recibe el id del post y retorna su infromación"""
    
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty")
    return response.json()
    
def extraer(list_ids: list, cantidad: int) -> list:
    """Hace 10 gets por seg y de cada id recibe la
    información del post"""
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        items = list(executor.map(obtener_item, list_ids[:cantidad]))
    return items

def leer_datos():
    """Intenta leer el archivo local, si no existe
    renorta una lista vacía"""
    try:
        with open("data/raw/items.json", "r", encoding="utf-8") as f:
            return json.load(f)       
    except FileNotFoundError:
        return []
    
def guardar(items: list):
    datos = leer_datos()
    datos.extend(items)
    with open("data/raw/items.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(datos, indent=2))
        print("Items guardados:", json.dumps(items, indent=2))
        
def main():
    ids = obtener_ids(10)
    items = extraer(list_ids=ids, cantidad=1)
    guardar(items)

main()

# Lecciones:
"""Se usan en diferentes ocasiones"""
#json.loads(f)  # ❌ f es un archivo, no un string
#json.load(f)   # ✅ f es un archivo