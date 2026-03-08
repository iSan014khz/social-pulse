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

def obtener_ids(cant_items: int):
    response = requests.get(f"{api}{end_point}").json()
    return response[:cant_items]

def obtener_item(id: int):
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty")
    return response.json()
    
def extraer(list_ids: list, cantidad: int) -> list:
    with ThreadPoolExecutor(max_workers=10) as executor:
        items = list(executor.map(obtener_item, list_ids[:cantidad]))
    return items

def guardar(items: list):
    try:
        with open("data/raw/items.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data.extend(items)
            with open("data/raw/items.json", "w", encoding="utf-8") as f:
                return f.write(json.dumps(data, indent=4))
            
    except (FileNotFoundError, json.JSONDecodeError):
        with open("data/raw/items.json", "w", encoding="utf-8") as f:
            return f.write(json.dumps(items, indent=4))
        
    
def main():
    ids = obtener_ids(10)
    items = extraer(list_ids=ids, cantidad=10)
    guardar(items)

main()