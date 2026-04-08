from pydantic import BaseModel, Field

from typing import Optional

class ScanCreate(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    location: str

class ScanInDB(ScanCreate):
    id: Optional[str] = Field(default=None, alias="_id")
    model_config = {"populate_by_name": True}