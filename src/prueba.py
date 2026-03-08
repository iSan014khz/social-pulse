from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

app_name = os.getenv("APP_NAME")
api = os.getenv("HN_BASE_URL")
end_point = os.getenv("HN_TOP_STORIES")
item = os.getenv("HN_ITEM")
max_post = os.getenv("MAX_POSTS")


response = requests.get(f"{api}{end_point}").text

lista = json.loads(response)[:int(5)]

print(lista, len(lista))



