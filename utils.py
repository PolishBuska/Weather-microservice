import json
import httpx
from database import SQLALCHEMY_DATABASE_URL
from config import settings
from fastapi_utils.session import FastAPISessionMaker
from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
import models

sessionmaker= FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)
def kelvin_to_celcium(response, city):
  response_1=response['main']['temp'] -273.15
  response_2=f"{response['weather'][0]['description']}"
  response={'city':f"{city}",
          'weather':f'{response_2}',
          'temperature':str(response_1)}
  return response
async def get_response(city: str):
 async with httpx.AsyncClient() as client:
    weather_city = f"{settings.url}appid={settings.api_key}&q={city}"
    response = await client.get(weather_city)
    response_json = json.loads(response.text)
    response_json_out = kelvin_to_celcium(response_json, city)
    return response_json_out

router = APIRouter(

)
@router.on_event("startup")
@repeat_every(seconds=60,wait_first=True)  # 1 hour
def del_weather():

    with sessionmaker.context_session() as db:


        response_out = db.query(models.City)
        response_out.delete(synchronize_session=False)
        db.commit()
    return