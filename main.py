from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from fastui.components.display import DisplayLookup
from pydantic import BaseModel, parse_obj_as
from typing import List, Annotated
from icecream import ic
from sqlmodel import Session, select
from database import engine, ShipDBModel, create_tables
from contextlib import asynccontextmanager
import json
from models import Ship, ShipForm

ships = None

seed_data='ships_full.json'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">> Lifespan")
    create_tables()

    with Session(engine) as session:
        stmt = select(ShipDBModel)
        res = session.exec(stmt).all()
        #ic(res)
        if res == None or len(res) < 1:
            ic(">> DB Empty, loading default set...")
            with open(seed_data, "r") as seed_content: 
                ship_data = json.load(seed_content)

                for s in ship_data:
                    ssm = ShipDBModel(**s)
                    ic(ssm)
                    session.add(ssm)
                    session.commit()

        elif res != None:
            ic(len(res))
            ic(f"found "+str(len(res))+" ships")
        
    yield

app = FastAPI(lifespan=lifespan)

async def get_db_session():
    with Session(engine) as session:
        yield session

def getShipsFromDB():
    with Session(engine) as session:
        stmt = select(ShipDBModel)
        res = session.exec(stmt).all()
    ic(f"ships from db: {ships}")
    return res

ship_json_old = [
        {"name": "Enterprise", "sign": "NX-01","classification": "Constitution", "speed": "Warp 1", "captain": "Jonathan Archer", "comment": "first warp capable ship"},
        {"name": "USS Enterprise", "sign": "NCC-1701","classification": "Constitution", "speed": "Warp 1", "captain": "Christopher Pike", "comment": ""},
        {"name": "USS Enterprise", "sign": "NCC-1701-D","classification": "Constitution", "speed": "Warp 1", "captain": "Jean Luc Picard", "comment": ""},
        {"name": "USS Franklin", "sign": "NX-326", "classification": "Starship", "speed": "Warp 4", "captain": "balthazar edison", "comment": "lost ~2160, first warp 4 capable ship"},
    ]

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
    """ 
    Show a table of ships, `/api` is the endpoint the frontend will connect to
    when a user visits `/`  to fetch components to render.
    """
    #ic(ships)
    #if len(ships) < 1:
    ships = getShipsFromDB()
    #ships = parse_obj_as(List[Ship], ship_json)
    
    
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
                    columns=[
                        DisplayLookup(field='sign'),   #, on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='name', on_click=GoToEvent(url='/ship/{id}/')),
                        DisplayLookup(field='captain'),# on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='classification'),  #, on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='speed'),  #on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='details') #on_click=GoToEvent(url='/ships/{id}/')),
                    ]
                ),
                c.Div(components=[
                    c.Link(
                        components=[c.Button(text='Add ship')],
                        on_click=GoToEvent(url='/ships/add')
                    )
                ])
            ]
        ),
    ]

@app.get('/api/ships/add', response_model=FastUI, response_model_exclude_none=True)
def add_ship():
    return [
        c.Page(components=[
            c.Heading(text='Add Ship', level=2),
            c.Paragraph (text='Add new Ship to th list'),
            c.ModelForm(model=ShipForm, submit_url='/api/ships/add')
        ])
    ]

@app.post("/api/ships/add")
async def create_ship(form: Annotated[ShipForm, fastui_form(ShipForm)], session : Session = Depends(get_session)): # -> FormResponse:
    ic(form)
    #ships.append(form)
    ship = ShipDBModel(**form.model_dump())
    session.add(ship)
    session.commit()
    #return

@app.get("/api/ships/{ship_id}/", response_model=FastUI, response_model_exclude_none=True)
def ship_profile(ship_id: int, session : Session = Depends(get_session)) -> list[AnyComponent]:
    """
    Ship profile page, the frontend will fetch this when the user visits `/ships/{id}/`.
    """
    #ship = session.get(ShipDBModel, ship_id)
    ship = ShipDBModel(**ship_json_old[0])
    """
    if ship is None:
        raise HTTPException(status_code=404, detail="Ship not found")

    return [
        c.Page(
            components=[
                c.Heading(text=ship.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=ship),
                c.Link(
                    components=[c.Text(text='Delete Ship')],
                    on_click=GoToEvent(url='/delete_ship/{ship_id}'),
                ),
            ]
        ),
    ] 
    """

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Intro with Startrek'))