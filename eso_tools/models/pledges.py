from pydantic import BaseModel

class PledgeList(BaseModel):
    giver: str
    dungeons: list[str]
