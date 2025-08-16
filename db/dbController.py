from re import M
from fastapi import APIRouter, Depends
from surrealdb import AsyncSurreal

from app.db.database import get_db

from app.db.dbSchema import Entry
from app.db.dbService import CreateEntryService

router = APIRouter(
    prefix="/db",
    tags=["db"],
)

@router.post("/")
async def create_entry(
        entry: Entry, 
        db: AsyncSurreal = Depends(get_db)
    ):
    return await CreateEntryService(
            entry,
            db
        )