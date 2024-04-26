from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from pydantic import BaseModel, parse_obj_as
from typing import List
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
import json
from database import DBShip, engine
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">> Lifespan")
    #create_tables()

class Ship(BaseModel):
     name: str
     sign:str
     classification: str
     captain: str = "n/a"
     speed: str = "n/a"
     comment: str = "n/a"

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI() #lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

ship_json = [
        {"name": "USS Enterprise", "sign": "NX-01","classification": "Constitution", "speed": "Warp 1", "captain": "Jonathan Archer", "comment": "first warp capable ship"},
        {"name": "USS Enterprise", "sign": "NCC-1701","classification": "Constitution", "speed": "Warp 1", "captain": "Christopher Pike", "comment": ""},
        {"name": "USS Enterprise", "sign": "NCC-1701-D","classification": "Constitution", "speed": "Warp 1", "captain": "Jean Luc Picard", "comment": ""},
        {"name": "USS Franklin", "sign": "NX-326", "classification": "Starship", "speed": "Warp 4", "captain": "balthazar edison", "comment": "lost ~2160, first warp 4 capable ship"},
    ]

def fetch_ships():
    print("1111")
    with Session(engine) as session:
        stmt = select(DBShip)
        res = session.exec(stmt).all()
    
    print(f"2222: {res}")
    ships = []
    if res is None or len(res) <= 1:
        print(f"3333: {res}")
        
        with Session(engine) as session:
            dbShip = DBShip(**ship_json[0])
            session.add(dbShip)
            dbShip = DBShip(**ship_json[1])
            session.add(dbShip)
            dbShip = DBShip(**ship_json[2])
            session.add(dbShip)
            dbShip = DBShip(**ship_json[3])
            session.add(dbShip)
            session.commit()
            stmt = select(DBShip)
            ships = session.exec(stmt).all()
    else:
        ships = res
        #print("4444")
        #seed_data='ships_full.json'
        #with open(seed_data, "r") as seed_content: 
        #    ship_data = json.load(seed_content)
        #ships = parse_obj_as(List[Ship], ship_data)
    
    return ships

def getShipsFromDB():
    with Session(engine) as session:
        stmt = select(DBShip)
        res = session.exec(stmt).all()
    return res


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
    """
    Show a table of ships, `/api` is the endpoint the frontend will connect to
    when a user visits `/`  to fetch components to render.
    """

    ships = fetch_ships()
    
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text=f'{len(ships)} Ships', level=2),  # renders `<h2>Ships</h2>`
                c.Image(
                    src='https://upload.wikimedia.org/wikipedia/commons/e/ef/Star_Trek_Logo.png',
                    alt='Startrek Logo',
                    width=800,
                    height=200,
                    loading='lazy',
                    referrer_policy='no-referrer',
                    class_name='border rounded',
                ),
                c.Table(
                    data=ships,
                    data_model=DBShip
                ),
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Intro with Startrek'))