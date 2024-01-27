from pydantic import BaseModel
from enum import Enum

class PenetrationBuff(BaseModel):
    name: str
    penetration: int