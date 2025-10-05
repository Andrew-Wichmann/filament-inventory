import fastapi
import uvicorn
import pydantic
from contextlib import asynccontextmanager
import logging
from models import FilamentInventory

logger = logging.getLogger('uvicorn')

@asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    logger.info("Init database")
    await inventory.init_db()
    logger.info("Database initialized")
    yield

app = fastapi.FastAPI(title="Filament Inventory", version="0.0.1", lifespan=lifespan)
inventory = FilamentInventory()

class Filament(pydantic.BaseModel):
    color: str

filaments: list[Filament] = []

@app.post("/api/filament/add")
async def add_filament(filament: Filament):
    filaments.append(filament)

@app.get("/api/filament/list")
async def list_filaments():
    return filaments

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_config='logging.yaml')
