from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from pydantic import BaseModel, parse_obj_as
from typing import List

app = FastAPI()

class Ship(BaseModel):
     name: str
     sign:str
     classification: str
     captain: str
     speed: str
     comment: str


ship_json = [
        {"name": "USS Enterprise", "sign": "NX-01","classification": "Constitution", "speed": "Warp 1", "captain": "Jonathan Archer", "comment": "first warp capable ship"},
        {"name": "USS Enterprise", "sign": "NCC-1701","classification": "Constitution", "speed": "Warp 1", "captain": "Christopher Pike", "comment": ""},
        {"name": "USS Enterprise", "sign": "NCC-1701-D","classification": "Constitution", "speed": "Warp 1", "captain": "Jean Luc Picard", "comment": ""},
        {"name": "USS Franklin", "sign": "NX-326", "classification": "Starship", "speed": "Warp 4", "captain": "balthazar edison", "comment": "lost ~2160, first warp 4 capable ship"},
    ]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
    """
    Show a table of ships, `/api` is the endpoint the frontend will connect to
    when a user visits `/`  to fetch components to render.
    """
    
    ships = parse_obj_as(List[Ship], ship_json)
    
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
                ),
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Intro with Startrek'))