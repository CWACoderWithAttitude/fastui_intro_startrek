from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

DB_FILE='ships.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

class ShipDBModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sign:str
    classification: str
    captain: str
    speed: str
    comment: str

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()