from pydantic import BaseModel

class ShipForm(BaseModel):
    name: str
    sign:str
    classification: str
    captain: str
    speed: str
    comment: str

class Ship(BaseModel):
    name: str
    sign:str
    classification: str
    captain: str
    speed: str
    comment: str
