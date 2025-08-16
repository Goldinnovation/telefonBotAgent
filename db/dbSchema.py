from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class PatientData(BaseModel):
    Name: str
    Geburtstag: str
    Nummer: str
    Dringlichkeit: str
    Untersuchung: str
    Tier: str
    Termin: str