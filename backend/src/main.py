from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

from .lib.firebase import init_firebase_app
init_firebase_app()

from firebase_admin import firestore_async
firestore = firestore_async.client()

from pydantic import BaseModel

app = FastAPI(root_path="/api")

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "技育CAMP2024ハッカソンVol.4 Topaz Taamagawa (Backend)"

@app.get("/users")
async def get_users():
    users_stream = firestore.collection("sample-users").stream()

    users = {}
    async for user_snpashot in users_stream:
        users[user_snpashot.id] = user_snpashot.to_dict()

    return users

class SampleUser(BaseModel):
    name: str

@app.post("/users")
async def post_users(user: SampleUser, user_id: str):
    users_ref = firestore.collection("sample-users")
    await users_ref.document(user_id).set(user.model_dump())
    return user_id
    