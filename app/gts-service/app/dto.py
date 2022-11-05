from pydantic import BaseModel, Json
from enum import Enum

class PlatformEnum(str, Enum):
    nds = "nds"
    flatpass = "flatpass"
    none = "none"

class TransferPlatformEnum(str, Enum):
    gts_nds = "gts-nds"
    nds_gts = "nds-gts"
    none = "none"

class FlatpassStatus(BaseModel):

    class ConnectionDetails(BaseModel):
        host: str
        port: str
        
    status: str
    platform: str
    connection_details: ConnectionDetails

class FlatpassTransfer(BaseModel):
    status: str
    transfer_platform: str
    details: str