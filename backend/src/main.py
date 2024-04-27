from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import random
from dotenv import load_dotenv

load_dotenv(verbose=True)

from .lib.firebase import init_firebase_app

init_firebase_app()

from firebase_admin import firestore_async

firestore = firestore_async.client()

from pydantic import BaseModel

app = FastAPI(root_path="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class SampleTask(BaseModel):
    name: str


async def read_task(tasks_id: str):
    task_ref = firestore.collection("sample-task").document(tasks_id)
    task = await task_ref.get()
    if task.exists:
        return task.to_dict()
    else:
        return None


@app.post("/users")
async def post_users(user: SampleUser, user_id: str):
    users_ref = firestore.collection("sample-users")
    await users_ref.document(user_id).set(user.model_dump())
    return user_id


@app.get("/tasks")
async def read_tasks():
    tasks_stream = firestore.collection("sample-task").stream()
    tasks = {}
    async for task_snpashot in tasks_stream:
        tasks[task_snpashot.id] = task_snpashot.to_dict()

    return tasks


@app.get("/tasks/{tasks_id}")
async def read_task_endpoit(tasks_id: str):
    return await read_task(tasks_id)


@app.post("/tasks")
async def post_task(task: SampleTask):
    while True:
        num = int((random.random() * 10) ** 10)
        tasks_id = str(num)
        juagetask = await read_task(tasks_id)
        if juagetask == None:
            task_ref = firestore.collection("sample-task")
            await task_ref.document(tasks_id).set(task.model_dump())
            return tasks_id


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    await firestore.collection("sample-task").document(task_id).delete()
