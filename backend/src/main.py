from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, time, timedelta
from typing import List, Optional

import os
import random
from dotenv import load_dotenv

load_dotenv(verbose=True)

from .lib.firebase import init_firebase_app

init_firebase_app()

from src.lib.auth import get_user, FirebaseUser

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


@app.get("/auth-ex")
async def get_users(user: FirebaseUser = Depends(get_user)):
    print(user)


@app.get("/users")
async def get_users():
    users_stream = firestore.collection("sample-users").stream()

    users = {}
    async for user_snpashot in users_stream:
        users[user_snpashot.id] = user_snpashot.to_dict()

    return users


class SampleUser(BaseModel):
    name: str
    age: int
    birth: str
    college: str
    Department: str


class InputTask(BaseModel):
    creat_at: datetime


class SampleTask(BaseModel):
    name: str
    user_id: str
    lesson_id: str
    By_date: Optional[datetime]


class SampleLesson(BaseModel):
    name: str
    place: str
    date: str
    date_index: int


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


@app.get("/users")
async def read_users():
    user_stream = firestore.collection("sample-users").stream()
    user = {}
    async for user_snpashot in user_stream:
        user[user_snpashot.id] = user_snpashot.to_dict()
    return user


@app.get("/user/{user_id}")
async def read_user(user_id: str):
    user_ref = firestore.collection("sample-users").document(user_id)
    user = await user_ref.get()
    if user.exists:
        return user.to_dict()
    else:
        return None


@app.post("/user/register")
async def register_post_user(user_id: str, age: int, colleg: str, depertment: str):
    user = await read_user(user_id)


@app.get("/profile")
async def read_user(id: str):
    user_ref = firestore.collection("sample-users").document(id)
    user = await user_ref.get()
    if user.exists:
        user_dict = user.to_dict()
        return user_dict
    else:
        return None


# すべてのタスクを取得
@app.get("/tasks")
async def read_tasks():
    tasks_stream = firestore.collection("sample-task").stream()
    tasks = {}
    async for task_snpashot in tasks_stream:
        tasks[task_snpashot.id] = task_snpashot.to_dict()

    return tasks


# 特定のタスクを取得
@app.get("/tasks/{tasks_id}")
async def read_task_endpoit(tasks_id: str):
    return await read_task(tasks_id)


# user登録情報を基にタスクを生成
@app.post("/tasks")
async def post_task(task: SampleTask, user_id: str, lesson_id: str, date: datetime):
    while True:
        num = int((random.random() * 10) ** 10)
        tasks_id = str(num)
        juagetask = await read_task(tasks_id)
        if juagetask == None:
            task_ref = firestore.collection("sample-task")
            task_dict = task.model_dump()
            task_dict["create_at"] = firestore_async.SERVER_TIMESTAMP
            task_dict["user_id"] = user_id
            task_dict["lesson_id"] = lesson_id
            task_dict["By_date"] = date

            await task_ref.document(tasks_id).set(task_dict)

            return tasks_id


# タスクidを基にタスクを削除
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    await firestore.collection("sample-task").document(task_id).delete()


@app.get("/users/{user_id}/share")
async def share(user_id: str):
    lesson_list = firestore.collection("lessons").where("user_id", "==", user_id)
    lessons = []
    async for lessons_snpashot in lesson_list.stream():
        lessons.append(lessons_snpashot.to_dict())
    lessons.sort(key=lambda l: l["date_index"])
    return lessons

@app.post("/lessons")
async def creat_lesson(
    lesson: SampleLesson,
    user: FirebaseUser = Depends(get_user),
):
    while True:
        num = int((random.random() * 10) ** 10)
        lesson_id = str(num)
        lesson_ref = firestore.collection("lessons").document(lesson_id)
        get_lesson = await lesson_ref.get()

        if get_lesson.exists:
            lesson_dict = lesson.model_dump()
            lesson_dict["user_id"] = user.uid
            await lesson_ref.set(lesson_dict)
            return lesson_id
