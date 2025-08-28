from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from surrealdb import AsyncSurreal
from typing import List, Optional
import uvicorn

from db.database import get_db
from db.dbService import CreateEntryService, GetEntryService
from db.dbSchema import PatientData

# Create FastAPI app
app = FastAPI(
    title="Telephony Bot API",
    description="API for managing patient appointments",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Telephony Bot API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "telephony-bot-api"}

@app.post("/patients")
async def create_patient(
    patient: PatientData,
    db: AsyncSurreal = Depends(get_db)
):
    """Create a new patient appointment"""
    try:
        result = await CreateEntryService(patient, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
async def get_all_patients(
    db: AsyncSurreal = Depends(get_db)
):
    """Get all patient appointments"""
    try:
        result = await GetEntryService(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients/count")
async def get_patient_count(
    db: AsyncSurreal = Depends(get_db)
):
    """Get the count of patient appointments"""
    try:
        result = await GetEntryService(db)
        return {"count": result["count"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/patients")
async def delete_all_patients(
    db: AsyncSurreal = Depends(get_db)
):
    """Delete all patient appointments (⚠️ Use with caution!)"""
    try:
        result = await db.query("DELETE FROM PatientenTermin;")
        return {"status": "success", "message": "All patients deleted", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
