from pydantic import BaseModel
from datetime import datetime

class Weather_out (BaseModel):
    city: str
    weather: str
    temperature: float
    wind: str
    class Config():
        orm_mode = True

class Weather_out_db (Weather_out):
    created_at: datetime
    class Config():
        orm_mode = True
