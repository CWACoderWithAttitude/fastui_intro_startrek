from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

DB_FILE='ships.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
NOT_KNOWN='n/n'
class ShipDBModel(SQLModel, table=True):
    id             : Optional[int] = Field(default=None, primary_key=True)
    name           : str
    sign           : str
    classification : str
    speed          : Optional[str] = Field(default=NOT_KNOWN)
    comment        : Optional[str] = Field(default=NOT_KNOWN)
    captain        : Optional[str] = Field(default=NOT_KNOWN)
    details        : Optional[str] = Field(default=NOT_KNOWN)

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()