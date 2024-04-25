from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

class Ship(BaseModel):
    id: int 
    name: str
    comment: Optional[str]

class ShipCreate(BaseModel):
    id: int 
    name: str
    comment: Optional[str]
