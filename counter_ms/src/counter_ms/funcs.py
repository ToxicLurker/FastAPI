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

import tarantool
import logging

app = FastAPI()


class MessageClass(BaseModel):
    sender_id: str
    reciever_id: str


@app.post("/dialog/increase_unread")
async def dialog_send_message(message: MessageClass):
    print('a')
    logging.info('b')
    return send_message(message.sender_id, message.reciever_id)


@app.get("/dialog/decrease_unread")
async def dialog_get_messages(message: MessageClass):
    return get_messages(message.sender_id, message.reciever_id)

