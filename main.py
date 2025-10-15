import fastapi
import uvicorn
from contextlib import asynccontextmanager
import logging
from models import AddFilamentRequest, Filament, ConsumeRequest
from filament_inventory import FilamentInventory, InventoryException

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    logger.info("Init database")
    await inventory.init_db()
    logger.info("Database initialized")
    yield


app = fastapi.FastAPI(title="Filament Inventory", version="0.0.1", lifespan=lifespan)
inventory = FilamentInventory()


@app.post("/api/filament")
async def add_filament(request: AddFilamentRequest) -> Filament:
    logger.info(f"Adding filament {request}")
    return await inventory.add(request.color, request.weight)


@app.get("/api/filament")
async def list_filaments() -> list[Filament]:
    return await inventory.list()


@app.post("/api/filament/consume")
async def consume_filament(request: ConsumeRequest) -> Filament:
    try:
        return await inventory.consume(request.filament_id, request.grams)
    except InventoryException as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


@app.get("/api/filament/{filament_id}")
async def get_filament(filament_id: int) -> Filament:
    try:
        return await inventory.get(filament_id)
    except InventoryException as e:
        raise fastapi.HTTPException(status_code=404, detail=str(e))


@app.delete("/api/filament/{filament_id}")
async def delete_filament(filament_id: int) -> dict:
    try:
        await inventory.delete(filament_id)
        return {"detail": "Filament deleted"}
    except InventoryException as e:
        raise fastapi.HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_config="logging.yaml")
