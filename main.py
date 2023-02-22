import asyncio as asyncio
import json
import time
from sqlalchemy import select
import httpx
import requests
import datetime
from typing import List
import models
from utils import kelvin_to_celcium
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








@app.middleware("http")
async def add_process_time_header(request,call_next):
    start_time = time.time()
    response = await  call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


async def get_response(city: str):
 async with httpx.AsyncClient() as client:
    weather_city = f"{settings.url}appid={settings.api_key}&q={city}"
    response = await client.get(weather_city)
    response_json = json.loads(response.text)
    response_json_out = kelvin_to_celcium(response_json, city)
    return response_json_out


@app.get("/weather/request/{city}",response_model=schemas.Weather_out)
async def get_weather(city: str,db: Session = Depends(get_db)):
    #one_city = db.query(models.city).where(city.name == name).first()




    response = await asyncio.gather(get_response(city))
    response_1 = dict(*response)

    db_response = (models.City(**dict(*response)))
    db.add(db_response)
    print(db_response)
    db.commit()
    db.refresh(db_response)

    return response_1

@app.get("/weather/{city}",
         response_model=List[schemas.Weather_out_db],
         description="Getting a city from the db"
         )
async def get_weather(city: str,db: Session = Depends(get_db)):
    #one_city = db.query(models.city).where(city.name == name).first()



    #weather_city = f"{URL}appid={API_KEY}&q={city}"

    #response = requests.get(weather_city).json()

    response_out = db.query(models.City)(models.City.city == city).all()
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









