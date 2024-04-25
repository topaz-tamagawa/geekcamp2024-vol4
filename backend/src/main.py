from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

from .lib.firebase import init_firebase_app
init_firebase_app()

from firebase_admin import firestore_async
firestore = firestore_async.client()

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "技育CAMP2024ハッカソンVol.4 Topaz Taamagawa (Backend)"
