from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class Entry(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None