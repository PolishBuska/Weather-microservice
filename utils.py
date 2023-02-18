from database import get_db
import models
from fastapi import Depends,BackgroundTasks
from sqlalchemy.orm import Session
def kelvin_to_celcium(response, city):
  response_1 = response['main']['temp'] -273.15
  response_2 =f"{response['weather'][0]['description']}"

  return {'city':f"{city}",
          'weather':f'{response_2}',
          'temperature':str(response_1)}


#def get_weather(city: str):  # db: Session = Depends(database.get_db)
    # one_city = db.query(models.city).where(city.name == name).first()

   # weather_city = f"{URL}appid={API_KEY}&q={city}"

  #  response = requests.get(weather_city).json()

    #response_out = kelvin_to_celcium(response, city)

    #return response_out



#async def get_weather(city: str):
  #  async with aiohttp.ClientSession() as session:
   #     weather_city = f"{URL}appid={API_KEY}&q={city}"
   #     async with session.get(weather_city) as resp:
    #        info = await resp.json()
      #  response = kelvin_to_celcium(resp,city)
      #  return response
def del_weather_2(db: Session = Depends(get_db)):

    response_out = db.query(models.City)
    response_out.delete(synchronize_session=False)
    db.commit()
