from datetime import datetime, timedelta
from typing import Union
from pydantic import BaseModel

import time

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import mysql.connector

from fastapi import FastAPI, Request

from .crud.crud_user import get_user, create_user, get_user_info, get_user_by_name, generate_numbers_func, send_message, get_messages, add_friend, delete_friend, create_post, feed_post, get_user_by_name_from_tarantool
from .models.token_modles import Token, TokenData
from .models.user_models import User, UserInDB
from .models.transmitions_models import MessageClass

import tarantool
import logging
import requests
import json

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30000





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(id=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/user/register")
async def register(id: str, password: str, first_name: str, second_name: Union[str, None] = None, age: Union[str, None] = None, birthdate: Union[str, None] = None, biography: Union[str, None] = None, city: Union[str, None] = None):
    if get_user(id):
        return "User is already exists!"
    a = UserInDB(id=id, first_name=first_name, second_name=second_name, age=age, birthdate=birthdate, biography=biography, city=city, hashed_password=get_password_hash(password), disabled=0)
    return create_user(a)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/user/get/{id}")
async def get_user_by_id(id: str, current_user: User = Depends(get_current_active_user)):
    return get_user_info(id)


@app.get("/user/search")
async def user_search(first_name: str, second_name: str, current_user: User = Depends(get_current_active_user)):
    return get_user_by_name(first_name.capitalize(), second_name.capitalize())

@app.get("/user/search_tar")
async def user_search_tar(first_name: str, second_name: str, current_user: User = Depends(get_current_active_user)):
    return get_user_by_name_from_tarantool(first_name.capitalize(), second_name.capitalize())


@app.get("/generate_numbers")
async def generate_numbers(current_user: User = Depends(get_current_active_user)):
    return generate_numbers_func()


@app.post("/dialog/{user_id}/send")
async def dialog_send_message(user_id: str, message: str, current_user: User = Depends(get_current_active_user)):
    msg = MessageClass(user_id=user_id, current_user=current_user.id, message=message)
    print(json.dumps(msg.dict()))
    r = requests.post(f'http://dialog_ms:12345/dialog/send', json=msg.dict())
    logging.info('r')
    logging.info(r)
    print(r)
    print(r.text)


@app.get("/dialog/{user_id}/list")
async def dialog_get_messages(user_id: str, current_user: User = Depends(get_current_active_user)):
    msg = MessageClass(user_id=user_id, current_user=current_user.id, message='', transaction_id = int(datetime.now().timestamp()))
    print(json.dumps(msg.dict()))
    r = requests.get(f'http://dialog_ms:12345/dialog/list', json=msg.dict())
    logging.info('r')
    logging.info(r)
    print(r)
    print(r.text)
    return r.text


@app.get("/friend/add")
async def add_friend_ep(user_friend_id: str, current_user: User = Depends(get_current_active_user)):
    return add_friend(current_user.id, user_friend_id)


@app.get("/friend/delete")
async def delete_friend_ep(user_friend_id: str, current_user: User = Depends(get_current_active_user)):
    return delete_friend(current_user.id, user_friend_id)

@app.get("/post/create")
async def post_create(post: str, current_user: User = Depends(get_current_active_user)):
    return create_post(current_user.id, post)


@app.get("/post/feed")
async def post_feed(current_user: User = Depends(get_current_active_user)):
    return feed_post(current_user.id)



@app.get("/user/show_index")
async def user_show_index(current_user: User = Depends(get_current_active_user)):
    connection = tarantool.connect("mytarantool", 3301)
    # tarantool.connect("mytarantool", 3301, user='guest', password='pass')
    tester = connection.space('users')
    with open('new_people.csv', 'r') as f:
        for i in f:
            record = i.split(',')
            print(type(record[0]))
            print(type(record[1]))
            print(type(record[2]))
            print(type(record[3]))
            print(type(record[4]))
            print(type(record[5]))
            print(type(record[6]))
            print(type(record[8]))
            print(record[0], record[1], record[2], record[3], record[4], record[5], record[6], int(record[8]))
            tester.insert((record[0], record[1], record[2], record[3], record[4], record[5], record[6], int(record[8])))
    return 'ok'
    # return show_index(first_name, second_name)