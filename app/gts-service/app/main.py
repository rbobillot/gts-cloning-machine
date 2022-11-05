import httpx
import json
import logging
import ormar
import socketio

from base64 import b64decode
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID

from app.db import Pokemon, database
from app.dto import FlatpassStatus, FlatpassTransfer, PlatformEnum, TransferPlatformEnum
from app.pkm_ser_de import pkm_to_json
from app.ws_events_handler import sio, connect_to_event_manager

FLATPASS_HOST = 'host.docker.internal'
FLATPASS_PORT = '8082'

logger = logging.getLogger("uvicorn")

app = FastAPI(title="FakeGTS API",
              description="A fake GTS API, and a cloning machine", version="0.2.1")

# Allow CORS for all origins (used for manual testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False)
async def status():
    return {"status": "ok"}

### Pokemon related endpoints ###

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

    After the pokemon is saved, the event manager is notified with a 'create-success' message 
    (so the front can display the created Pokemon)
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
    try:
        await pokemon.save()
        await sio.emit('flatpass-transfer', json.dumps({
            'status': 'create-success',
            'transfer_platform': 'nds-gts',
            'details': f'{pokemon.raw_pkm_data}'
        }), namespace='/gts-service')
        return pokemon
    except Exception as exc: # TODO: Handle more exceptions (cannot save pokemon, cannot emit event)
        await sio.emit('flatpass-transfer', json.dumps({
            'status': 'error',
            'transfer_platform': 'nds-gts',
            'details': 'Error while saving pokemon' # TODO: add more details
        }), namespace='/gts-service')
        raise HTTPException(status_code=500, detail=str(exc))

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

### Flatpass related endpoints ###

@app.get("/flatpass/status")
async def flatpass_status(platform: PlatformEnum):
    try:
        return httpx.get(
            f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/status/{platform}',
            timeout=None).json()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail="GTS flatpass is not running")

@app.get("/flatpass/transfer/status", include_in_schema=False)
async def transfer_status():
    try:
        return httpx.get(
            f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/transfer/status',
            timeout=None).json()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail="GTS flatpass is not running")

@app.post("/flatpass/transfer")
async def transfer_pokemon(pokemon: Pokemon | dict, transfer_platform: TransferPlatformEnum = None, gen: int = 4):
    """
    Platform can either be:
    - gts-nds
    - nds-gts
    """
    if transfer_platform is None:
        raise HTTPException(status_code=400, detail="Missing platform")
    if gen != 4:
        raise HTTPException(status_code=400, detail=f"Gen {gen} if not supported yet")

    try:
        # If the pokemon is a dict, it is assumed to be an empty json object
        if isinstance(pokemon, dict) and transfer_platform == TransferPlatformEnum.nds_gts:
            httpx.post(
                f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/transfer/gen-{gen}/{transfer_platform}',
                json={},
                timeout=None)
        elif isinstance(pokemon, Pokemon) and transfer_platform == TransferPlatformEnum.gts_nds:
            httpx.post(
                f'http://{FLATPASS_HOST}:{FLATPASS_PORT}/transfer/gen-{gen}/{transfer_platform}',
                json=jsonable_encoder(pokemon),
                timeout=None)
            try:
                await pokemon.save()
            except:
                logger.warning(f"Pokemon {pokemon.id} already exists")
        else:
            raise HTTPException(status_code=400, detail="Invalid data")
        return pokemon
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail="GTS flatpass is not running")

### Event-manager related endpoints ###

@app.post("/event/flatpass/status")
async def event_flatpass_status(data: FlatpassStatus):
    """
    Receives statuses:
    - flatpass: started / stopped
    - NDS: connected / disconnected (not handled yet)
    and notifies the gts-event-manager via socketio
    which will then notify the frontend
    """
    try:
        await sio.emit('flatpass-status', data.json(), namespace='/gts-service')
        return {"info": "notified statuses about flatpass to event-manager", "data": data.json()}
    except socketio.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500, detail="SocketIO connection error")

@app.post("/event/flatpass/transfer")
async def event_flatpass_transfer(data: FlatpassTransfer):
    try:
        await sio.emit('flatpass-transfer', data.json(), namespace='/gts-service')
        return {"info": "notified nds-to-gts transfer status to event-manager", "data": data.json()}
    except socketio.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500, detail="SocketIO connection error")


"""
DB startup / shutdown events handling
"""


@app.on_event("startup")
async def startup():
    await connect_to_event_manager()
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
