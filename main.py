import time
from fastapi import FastAPI
from database import SQLALCHEMY_DATABASE_URL
from fastapi_utils.session import FastAPISessionMaker
from routs import weather
import utils
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi.responses import FileResponse
import os

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

app = FastAPI(
    title="Box's MS for weather"
)
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

app.include_router(weather.router)
app.include_router(utils.router)


app.mount("/static", StaticFiles(directory="static"),name="static")


@repeat_every(seconds=1,wait_first=False)
@app.on_event("startup")
@app.get("/static/static.jpg")
def get_img(filename='static.jpg'):
    filepath = os.path.join('static/', os.path.basename(filename))
    return FileResponse(filepath)

@app.get("/")
def image(filename='static.jpg'):
    filepath = os.path.join('static/', os.path.basename(filename))
    return FileResponse(filepath)