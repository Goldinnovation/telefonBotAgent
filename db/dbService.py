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


async def GetEntryService(db=None):
    """Get all entries from the database"""
    try:    
        # If no db is provided, get one
        if db is None:
            db = await get_db()
            
        print("GetEntryService: Fetching all entries")    
        
        # Query all records from PatientenTermin table
        result = await db.query("SELECT * FROM PatientenTermin;")
        print("Query result:", result)
        
        # Handle SurrealDB query result format
        if result and len(result) > 0:
            # SurrealDB returns results in a specific format
            entries = result[0].get("result", []) if isinstance(result[0], dict) else result
            count = len(entries) if isinstance(entries, list) else 0
        else:
            entries = []
            count = 0
            
        return {
            "status": "success", 
            "entries": entries,
            "count": count
        }

    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")