from app.pkm_ser_de import pkm_to_json
import httpx
import ormar
from base64 import b64encode, b64decode
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID

from app.db import Pokemon, database

# FLATPASS_<HOST|PORT> will be used when flat-pass is dockerized
FLATPASS_HOST = 'host.docker.internal'
FLATPASS_PORT = '8082'

app = FastAPI(title="FakeGTS API",
              description="A fake GTS API, and a cloning machine", version="0.0.2")

# Allow CORS for all origins (used for manual testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False)
async def root():
    return {"status": "ok"}


@app.get("/flatpass-status")
async def flatpass_status():
    """
    Returns the status from the GTS flatpass
    GTS flasspass is running on the computer's localhost
    which is reached through the host.docker.internal
    """
    try:
        return httpx.get(
            f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/status',
            timeout=1.0).json()
    except httpx.RequestError as exc:
        return {"isRunning": False, "status": None}


@app.get("/flatpass-receive")
async def receive_pokemon_from_flatpass():
    try:
        return httpx.get(
            f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/receive',
            timeout=None).json()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail="GTS flatpass is not running")


@app.post("/flatpass-send")
async def send_pokemon_to_flatpass(pokemon: Pokemon):
    try:
        httpx.post(
            f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/send',
            json=jsonable_encoder(pokemon),
            timeout=None)
        # handle the case where a pokemon already exists with the same id
        try:
            await pokemon.save()
        except:
            print(f"Pokemon {pokemon.id} already exists")
        return pokemon
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail="GTS flatpass is not running")


@app.get("/pokemon")
async def get_all_pokemon(name: str = None):
    """
    Returns all pokemon in the database
    """
    if name:
        return await Pokemon.objects.filter(name__icontains=name).all()
    return await Pokemon.objects.all()


@app.get("/pokemon/{id}")
async def get_pokemon(id: UUID):
    """
    Returns a pokemon by id
    """
    try:
        return await Pokemon.objects.get(id=id)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail="Pokemon not found")


@app.post("/pokemon", status_code=201)
async def create_pokemon(pkm_data: Pokemon | str):
    """
    Creates a pokemon in the database
     - If the received data is a string, it is assumed to be a base64 encoded string.
       Hense, it is decoded and converted to a Pokemon object, and then saved to the database
     - If the received data is a Pokemon object, it is directly saved to the database
    """
    if isinstance(pkm_data, str):
        try:
            pkm_json = pkm_to_json(b64decode(pkm_data))
            pokemon = Pokemon(**pkm_json)
        except Exception as exc:
            raise HTTPException(
                status_code=400, detail="Invalid pokemon data")
    elif isinstance(pkm_data, Pokemon):
        pokemon = pkm_data
    else:
        raise HTTPException(status_code=400, detail="Invalid data")
    await pokemon.save()
    return pokemon


@app.put("/pokemon/{id}", status_code=201)
async def update_pokemon(id: UUID, pokemon: Pokemon):
    # await Pokemon.objects.get(id=id)
    # await pokemon.save()
    return pokemon


@app.delete("/pokemon/{id}", status_code=204)
async def delete_pokemon(id: UUID):
    try:
        pokemon = await Pokemon.objects.get(id=id)
        await pokemon.delete()
        return {"status": "ok"}
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail="Pokemon not found")

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
