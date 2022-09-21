import uuid
from fastapi import FastAPI
from uuid import UUID

from app.db import Pokemon, database

app = FastAPI(title="FakeGTS API",
              description="A fake GTS API, and a cloning machine", version="0.0.1")


@app.get("/health")
async def root():
    return {"status": "ok"}


@app.get("/pokemon/")
async def get_pokemon():
    return await Pokemon.objects.all()


@app.get("/pokemon/{id}")
async def get_pokemon(id: UUID):
    return await Pokemon.objects.get(id=id)


@app.post("/pokemon/")
async def create_pokemon(pokemon: Pokemon):
    await pokemon.save()
    return pokemon


@app.put("/pokemon/{id}")
async def update_pokemon(id: UUID, pokemon: Pokemon):
    await Pokemon.objects.get(id=id)
    await pokemon.save()
    return pokemon


@app.delete("/pokemon/{id}")
async def delete_pokemon(id: UUID):
    pokemon = await Pokemon.objects.get(id=id)
    await pokemon.delete()
    return {"status": "ok"}

"""
DB startup / shutdown events handling
"""


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
