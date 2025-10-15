import requests
from models import Filament, ConsumeRequest, AddFilamentRequest
import sys

if sys.argv[1] == "a":
    resp = requests.post(
        "http://localhost:8888/api/filament/add",
        json=AddFilamentRequest(color="red", weight=1000).model_dump(),
    )
elif sys.argv[1] == "l":
    resp = requests.get("http://localhost:8888/api/filament/list")
elif sys.argv[1] == "g":
    resp = requests.get("http://localhost:8888/api/filament/get?filament_id=1")
elif sys.argv[1] == "c":
    resp = requests.post(
        "http://localhost:8888/api/filament/consume",
        json=ConsumeRequest(filament_id=1, grams=10).model_dump(),
    )
else:
    resp = requests.get("http://localhost:8888/api/filament/list")


print(resp.json())
