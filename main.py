import asyncio as asyncio
import requests
import datetime
from typing import List
import models
from utils import kelvin_to_celcium,del_weather_2
from fastapi import FastAPI,Depends
import schemas
from fastapi import HTTPException,status
import aiohttp
import asyncio
from database import get_db,SQLALCHEMY_DATABASE_URL
from sqlalchemy.orm import Session
from config import settings
from fastapi_utils.tasks import repeat_every
from fastapi_scheduler import SchedulerAdmin
from fastapi_utils.session import FastAPISessionMaker
sessionmaker= FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)





app = FastAPI()

#weather_city = URL + "appid=" + API_KEY + "&q= London"

#response = requests.get(weather_city).json()
#hi = response['main']['temp'] - 100
#print(hi)

@app.get("/weather/request/{city}",response_model=schemas.Weather_out)
def get_weather(city: str,db: Session = Depends(get_db)):
    #one_city = db.query(models.city).where(city.name == name).first()



    weather_city = f"{settings.url}appid={settings.api_key}&q={city}"

    response = requests.get(weather_city).json()

    response_out = kelvin_to_celcium(response, city)
    db_response= models.City(**response_out)

    db.add(db_response)
    db.commit()
    db.refresh(db_response)

    return response_out

@app.get("/weather/{city}",
         response_model=List[schemas.Weather_out_db],
         description="Getting a city from the db"
         )
def get_weather(city: str,db: Session = Depends(get_db)):
    #one_city = db.query(models.city).where(city.name == name).first()



    #weather_city = f"{URL}appid={API_KEY}&q={city}"

    #response = requests.get(weather_city).json()

    response_out = db.query(models.City).filter(models.City.city == city).all()
    if not response_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{city} weather doesn't exist or isn't in the db")
    return response_out

@app.on_event("startup")
@repeat_every(seconds=60,wait_first=True)  # 1 hour
def del_weather():

    with sessionmaker.context_session() as db:


        response_out = db.query(models.City)
        response_out.delete(synchronize_session=False)
        db.commit()
    return












