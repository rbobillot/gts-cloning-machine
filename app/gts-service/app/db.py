from email.policy import default
from enum import unique
from uuid import UUID
import databases
import ormar
import pydantic
import sqlalchemy
import typing

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Pokemon(ormar.Model):
    class Meta(BaseMeta):
        tablename = "pokemon"

    # simple uuid primary key, making each pokemon unique
    id: UUID = ormar.UUID(primary_key=True,
                          unique=True,
                          nullable=False)
    checksum: str = ormar.String(max_length=32)
    name: str = ormar.String(max_length=32)
    index: int = ormar.Integer()
    holding: str = ormar.String(max_length=32)
    shiny: bool = ormar.Boolean()
    level: int = ormar.Integer()
    happiness: int = ormar.Integer()
    nature: str = ormar.String(max_length=32)
    species: str = ormar.String(max_length=32)
    ability: str = ormar.String(max_length=32)
    gender: str = ormar.String(max_length=32)
    ot: str = ormar.String(max_length=32)
    tid: int = ormar.Integer()
    sid: int = ormar.Integer()
    hidden_power: pydantic.Json = ormar.JSON(default={})
    moves: pydantic.Json = ormar.JSON(default=[])
    ivs: pydantic.Json = ormar.JSON(default={})
    evs: pydantic.Json = ormar.JSON(default={})
    original_language: str = ormar.String(max_length=32)
    modified_fields: pydantic.Json = ormar.JSON([])
    # base64 encoded string, from a 236 bytes buffer, describing a pokemon data (in pkm format)
    raw_pkm_data: str = ormar.String(max_length=512,
                                     unique=True,
                                     nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
