import functools
import os

from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

import logging
import psycopg2
import redis

# turn on logging
logging.basicConfig(level=logging.DEBUG)

# import environment variables
PG_SERVICE_URI = os.getenv('PG_SERVICE_URI')
REDIS_SERVICE_URI = os.getenv('REDIS_SERVICE_URI')

CACHE_TIMEOUT_SECONDS = 120
cache_timeout_str = os.getenv('CACHE_TIMEOUT_SECONDS', str(CACHE_TIMEOUT_SECONDS))
try:
    CACHE_TIMEOUT_SECONDS = int(cache_timeout_str)
except ValueError as e:
    logging.error(f'Bad value {cache_timeout_str}, using {CACHE_TIMEOUT}')
logging.info(f'Cache timeout is {CACHE_TIMEOUT_SECONDS}s')

CACHE_KEY_FORMAT = 'num_orders:{0}'

app = FastAPI()


def connect_to_pg():
    """Connect to the PostgreSQL backend."""
    if not PG_SERVICE_URI:
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Database not specified - "
            "environment variable PG_SERVICE_URI is empty/unset",
        )
    try:
        # Use the given service URI, but specify a different database
        return psycopg2.connect(PG_SERVICE_URI)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to database: {e.__class__.__name__} {e}",
        )


def connect_to_redis():
    """Connect to the Redis backend."""
    if not REDIS_SERVICE_URI:
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Redis service not specified - "
            "environment variable REDIS_SERVICE_URI is empty/unset",
        )
    try:
        # return redis.from_url(REDIS_SERVICE_URI)
        return redis.Redis(host='cache', port=6379)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to Redis: {e.__class__.__name__} {e}",
        )


def check_feed(func):
    @functools.wraps(func)
    def wrapper(user_id: str, *args, **kwargs):
        redis_conn = connect_to_redis()
        print('HUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
        print(redis_conn)

        cache_key = CACHE_KEY_FORMAT.format('' if user_id is None else user_id)

        logging.debug(f'Checking cache key {cache_key}')

        # Is it already in the cache? If so, just use it
        user_feed = redis_conn.get(cache_key)
        if user_feed:
            logging.debug(f'Found {cache_key}, value is {user_feed}')
            return user_feed

        logging.debug(f'Calling {func} to find the feed')
        retval = func(user_feed)

        # Remember to add it to the cache
        logging.debug(f'Caching {cache_key}, value is {retval}')
        # redis_conn.set(cache_key, retval, ex=CACHE_TIMEOUT_SECONDS)

        return retval

    return wrapper


# @app.get("/count")
@check_feed
def read_feed(user_id: str):
    pg_conn = connect_to_pg()
    try:
        cursor = pg_conn.cursor()
        logging.debug('Looking up for feed')
        cursor.execute(f"""SELECT post FROM posts WHERE user_id in (
                        SELECT user_friend_id FROM friends where user_id = '{user_id}')
                        order by ts desc
                        limit 1000;""")
        feed = cursor.fetchall()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying database: {e.__class__.__name__} {e}",
        )
    finally:
        pg_conn.close()

    return feed


def cache_post_feed(user_id: str, post:str, ts:int, *args, **kwargs):
    redis_conn = connect_to_redis()
    print('HUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
    print(redis_conn)

    pg_conn = connect_to_pg()
    try:
        cursor = pg_conn.cursor()
        logging.debug('Looking up for friends')
        cursor.execute(f"""SELECT user_friend_id FROM friends where user_id = '{user_id}';""")
        friends = cursor.fetchall()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying database: {e.__class__.__name__} {e}",
        )
    finally:
        pg_conn.close()

    for f in friends:
        cache_key = CACHE_KEY_FORMAT.format('' if f is None else f)

        logging.debug(f'Checking cache key {cache_key}')

        # Is it already in the cache? If so, just use it
        user_feed = redis_conn.get(cache_key)
        if user_feed:
            logging.debug(f'Found {cache_key}, value is {user_feed}')
            if len(user_feed[f]) == 1000:
                user_feed[f].pop(-1)
                user_feed[f].append([f, post, ts])
                redis_conn.set(cache_key, str(user_feed[f]))
                continue

        # logging.debug(f'Calling {func} to find the feed')
        redis_conn.set(cache_key, str([user_id, post, ts]))

        # Remember to add it to the cache
        # logging.debug(f'Caching {cache_key}, value is {retval}')
        # redis_conn.set(cache_key, retval, ex=CACHE_TIMEOUT_SECONDS)

    # return retval


