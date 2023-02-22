from typing import List
import models
from utils import get_response
from fastapi import Depends
import schemas
from fastapi import HTTPException,status,APIRouter
import asyncio
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/weather",
    tags=['getting_weather']
)
@router.get("/{city}",
         response_model=List[schemas.Weather_out_db],
         description="Getting a city from the db"
            )
def get_weather(city: str, db: Session = Depends(get_db)):
    response_out = db.query(models.City).filter(models.City.city == city).all()
    if not response_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{city} weather doesn't exist or isn't in the db")
    return response_out




@router.get("/request/{city}",response_model=schemas.Weather_out)
async def get_weather(city: str, db: Session = Depends(get_db)):
    response = await asyncio.gather(get_response(city))
    response_1 = dict(*response)
    db_response = (models.City(**dict(*response)))
    db.add(db_response)
    print(db_response)
    db.commit()
    db.refresh(db_response)

    return response_1
