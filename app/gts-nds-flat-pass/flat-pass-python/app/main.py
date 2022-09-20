from fastapi import FastAPI
from uuid import UUID

app = FastAPI(title="FastAPI, Docker, and Traefik")

@app.get("/")
async def root():
    return { "status" : "ok" }

@app.get("/pokemon/{pid}")
async def get_user(pid: UUID):
    return { "user_id" : pid }

"""
DB startup / shutdown events handling
"""

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
        # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
