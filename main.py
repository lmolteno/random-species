from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, text
from pydantic import BaseModel

sqlite_file_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

class Species(BaseModel):
    name: str
    genericName: str
    author: Optional[str] = None
    subgenus: Optional[str] = None
    genus: Optional[str] = None
    subtribe: Optional[str] = None
    tribe: Optional[str] = None
    subfamily: Optional[str] = None
    family: Optional[str] = None
    superfamily: Optional[str] = None
    order: Optional[str] = None
    remarks: Optional[str] = None

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

app.frontend("/", directory="static")

query = 'SELECT "dwc:scientificName", "dwc:genericName", "dwc:scientificNameAuthorship", "dwc:subgenus", "dwc:genus", "dwc:subtribe", "dwc:tribe", "dwc:subfamily", "dwc:family", "dwc:superfamily", "dwc:order", "dwc:class", "dwc:phylum", "dwc:kingdom", "dwc:taxonRemarks" FROM taxons WHERE "dwc:taxonRank" = "species" AND "dwc:class" = :class_name AND "dwc:taxonomicStatus" = "accepted" ORDER BY RANDOM() LIMIT 1;'

@app.get("/query")
def read_species(class_name: str, session: SessionDep):
    res = session.exec(text(query), params={"class_name": class_name}).fetchone()
    sciName, genericName, sciAuthor, subgenus, genus, subtribe, tribe, subfamily, family, superfamily, order, taxon_class, phylum, kingdom, remarks = res
    if sciAuthor is not None:
        name = sciName.replace(sciAuthor, "").strip()
    else:
        name = sciName
    species = Species(name=name, genericName=genericName, author=sciAuthor, subgenus=subgenus, genus=genus, subtribe=subtribe, tribe=tribe, subfamily=subfamily, family=family, superfamily=superfamily, order=order, remarks=remarks)
    return species
