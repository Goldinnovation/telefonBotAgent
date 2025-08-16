from db.database import get_db
from db.dbSchema import PatientData

async def CreateEntryService(
        entry, 
        db=None
    ):
    """Create an entry in the database"""
    try:    
        # If no db is provided, get one
        if db is None:
            db = await get_db()
            
        print("CreateEntryService: ", entry)    
        
        # Convert PatientData object to dictionary
        entry_data = entry.dict()
        
        # Add today's date and time
        from datetime import datetime
        entry_data["created_datetime"] = datetime.now().isoformat()

        result = await db.create("PatientenTermin", entry_data)
        
        return {
            "status": "success", 
            "result": result
        }

    except Exception as e:
        raise Exception(f"Database operation failed: {str(e)}")