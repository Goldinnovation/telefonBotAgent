from fastapi import HTTPException
from surrealdb import RecordID

async def CreateEntryService(entry, db):
    try:        
        # Prepare the data for database insertion using the simple Entry schema
        entry_data = {
            "name": entry.name,
            "value": entry.value,
        }
                
        result = await db.create("entry", entry_data)
        
        return {
            "status": "success", 
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")