import time
from fastapi import FastAPI
from database import SQLALCHEMY_DATABASE_URL
from fastapi_utils.session import FastAPISessionMaker
from routs import weather
import utils
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
