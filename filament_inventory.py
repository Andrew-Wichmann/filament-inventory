import aiosqlite
from models import Filament


class FilamentInventory:
    TABLE_NAME = "FILAMENT"

    def __init__(self):
        self.db = "filament.db"

    async def init_db(self):
        async with aiosqlite.connect(self.db) as conn:
            await conn.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                weight INTEGER NOT NULL
            )"""
            )
            await conn.commit()

    async def add(self, color: str, weight: int) -> Filament:
        async with aiosqlite.connect(self.db) as conn:
            cursor = await conn.execute(
                f"""INSERT INTO {self.TABLE_NAME} (color, weight) VALUES (?, ?)""",
                (color, weight),
            )
            await conn.commit()
            return Filament(id=cursor.lastrowid, color=color, weight=weight)  # type: ignore

    async def list(self) -> list[Filament]:
        async with aiosqlite.connect(self.db) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(f"""SELECT * FROM {self.TABLE_NAME}""")
            filaments = await cursor.fetchall()
            return [
                Filament(
                    id=filament["id"],
                    color=filament["color"],
                    weight=filament["weight"],
                )
                for filament in filaments
            ]

    async def get(self, filament_id: int) -> Filament:
        async with aiosqlite.connect(self.db) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.execute(
                f"""SELECT * FROM {self.TABLE_NAME} WHERE ID = ?""", (filament_id,)
            )
            filament = await cursor.fetchone()
            if filament is not None:
                return Filament(
                    id=filament["id"],
                    color=filament["color"],
                    weight=filament["weight"],
                )
            else:
                raise InventoryException(
                    f"Filament with id {filament_id} does not exist"
                )

    async def consume(self, filament_id: int, grams: int) -> Filament:
        filament = await self.get(filament_id)
        if filament.weight < grams:
            raise InventoryException(
                f"Filament with id {filament.id} does not have enough to be consumed. Filament remaining {filament.weight} grams"
            )
        filament.weight -= grams
        await self.__update(filament)
        return filament

    async def delete(self, filament_id: int):
        async with aiosqlite.connect(self.db) as conn:
            cursor = await conn.execute(
                f"""DELETE FROM {self.TABLE_NAME} WHERE id=?""", (filament_id,)
            )
            await conn.commit()
            if cursor.rowcount == 0:
                raise InventoryException(f"Filament {filament_id} not found")

    async def __update(self, filament: Filament) -> Filament:
        async with aiosqlite.connect(self.db) as conn:
            await conn.execute(
                f"""UPDATE {self.TABLE_NAME} SET color=?, weight=? WHERE id=?""",
                (filament.color, filament.weight, filament.id),
            )
            await conn.commit()
        return filament


class InventoryException(Exception):
    pass
