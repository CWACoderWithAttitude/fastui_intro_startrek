from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from pydantic import BaseModel
from typing import List, Annotated
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
import json
from database import DBShip, engine, create_tables
from sqlmodel import Session, select
from fastui.forms import SelectSearchResponse, fastui_form
from fastui.events import GoToEvent
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
#app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def read_ships(): #session : Session = Depends(get_session)):
    create_tables()


def fetch_ships():
    with Session(engine) as session:
        stmt = select(DBShip)
        res = session.exec(stmt).all()
    
    ships = []
    if res is None or len(res) <= 10:
        print(f"3333: {res}")
        
        with Session(engine) as session:
            seed_data='ships_full.json'
            with open(seed_data, "r") as seed_content: 
                temp = seed_content.read()
                ships_list = json.loads(temp)
                for ship in ships_list:
                    dbShip = DBShip(**ship)
                    print(f"ship2: {dbShip}")
                    session.add(dbShip)
                    
                session.commit()
                ships = session.exec(stmt).all()
    else:
        ships = res
    
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
                c.Div(components=[
                    c.Link(
                        components=[c.Button(text='Add ship')],
                        on_click=GoToEvent(url='/ships/add')
                    )
                ]),
                c.Table(
                    data=ships,
                    data_model=DBShip
                ),
            ]
        ),
    ]

@app.post("/api/ships/add")
async def create_ship(form: Annotated[Ship, fastui_form(Ship)], session : Session = Depends(get_session)): # -> FormResponse:
    print(form)
    ship = DBShip(**form.model_dump())
    session.add(ship)
    session.commit()
    session.close()

    # id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'name'))
    # return
    # ship = StartrekShipModel(**form.model_dump()) # unpack... (pydantic function)
    # session.add(ship)
    # session.commit()
    #ships.append(ship)
    #return SelectSearchResponse(event=GoToEvent('/'))



@app.get('/api/ships/add', response_model=FastUI, response_model_exclude_none=True)
def add_ship():
    return [
        c.Page(components=[
            c.Heading(text='Add Ship', level=2),
            c.Paragraph (text='Add new Ship to th list'),
            c.ModelForm(model=Ship, submit_url='/api/ships/add')
        ])
    ]
@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Intro with Startrek'))