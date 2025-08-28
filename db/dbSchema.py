from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class PatientData:
    Name: str
    Geburtstag: str
    Nummer: str
    Dringlichkeit: str
    Untersuchung: str
    Tier: str
    Termin: str