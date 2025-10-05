import requests
from main import Filament
import sys

if sys.argv[1] == 'a':
    resp = requests.post("http://localhost:8888/api/filament/add", json=Filament(color="red").model_dump())
elif sys.argv[1] == 'l':
    resp = requests.get("http://localhost:8888/api/filament/list")

print(resp.json())

