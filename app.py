from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from Network.exception.exception import NetworkException
from Network.logging.logger import logging
from Network.pipeline.training_pipeline import TrainPipeline
from Network.Constants import APP_HOST, APP_PORT

from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)