import logging
import socketio
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn")

app = FastAPI(title="GTS Event Manager",
              description="A small service to handle async events", version="0.0.1")

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='asgi')

# Allow CORS for all origins (used for manual testing)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"], # cors must be set, once, on AsyncServer instance (see above)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/', socketio.ASGIApp(sio))
app.mount('/socket.io/', socketio.ASGIApp(sio))
app.mount('/flatpass-status', socketio.ASGIApp(sio))


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}


@sio.on('flatpass-status', namespace='/gts-service')
async def notify_flatpass_status_to_front(sid, data):
    """
    Notify the front-end that the flatpass status has changed
    - flatpass app started or stopped
    - NDS is connected or disconnected (not handled yet)
    """
    logger.info(f"Received flatpass-status event from {sid} with data {data}")
    try:
        logger.info('Sending flatpass-status event to front')
        await sio.emit('flatpass-status', data, namespace='/gts-front')
    except Exception as e:
        logger.error(f"Error while emitting flatpass-status event to front: {e}")

@sio.on('flatpass-transfer', namespace='/gts-service')
async def notify_flatpass_transfer_to_front(sid, data):
    logger.info(f"Received flatpass-transfer event from {sid} with data {data}")
    try:
        logger.info('Sending flatpass-transfer event to front')
        await sio.emit('flatpass-transfer', data, namespace='/gts-front')
    except Exception as e:
        logger.error(f"Error while emitting flatpass-transfer event to front: {e}")


@sio.on('connect', namespace='/gts-service')
async def connect(sid, environ):
    logger.info(f"New client connected to gts-service namespace: {sid}")

@sio.on('connect', namespace='/gts-front')
async def connect(sid, environ):
    logger.info(f"New client connected to gts-front namespace: {sid}")


@sio.event
def connect(sid, environ, auth):
    logger.info('connected: ', sid)

@sio.event
def disconnect(sid):
    logger.info('disconnected: ', sid)

"""
startup / shutdown events handling
"""


@app.on_event("startup")
async def startup():
    logger.info('app startup')


@app.on_event("shutdown")
async def shutdown():
        logger.info('app shutdown')

