import psycopg2
from ..models.user_models import UserInDB, User
from contextlib import contextmanager
import logging
import time
from datetime import datetime
import pika
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
import tarantool
from ..cache.cache_functions import read_feed, cache_post_feed

def on_message(
        channel: BlockingChannel,
        method: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes):
    # print(channel)
    # print(method)
    # print(properties)
    print(body.decode('utf-8'))
    # если auto_ack=False (ниже), нужно вернуть положительное
    # (ack) или отрицательное подтверждение (nack)
    # во втором случае сообщение отправляется обратно в очередь
    # и будет возвращено с redelivered=True
    # channel.basic_nack(delivery_tag=method.delivery_tag)
    # channel.basic_ack(delivery_tag=method.delivery_tag)

@contextmanager
def managed_resource():
    cnx =  psycopg2.connect(host="pgmaster", user='admin', password='admin', dbname='dev', port=5432)
    cursor = cnx.cursor()
    try:
        yield (cursor, cnx)
    finally:
        cursor.close()
        cnx.close()


@contextmanager
def connect_to_replica():
    cnx =  psycopg2.connect(host="haproxy", user='admin', password='admin', dbname='dev', port=80)
    cursor = cnx.cursor()
    try:
        yield (cursor, cnx)
    finally:
        cursor.close()
        cnx.close()


def generate_numbers_func():
    with managed_resource() as (cursor, cnx):
        for i in range(60):
            cursor.execute(f"insert into test values ({i});")
            cnx.commit()
            print(f"insert into test values ({i});")
            time.sleep(1)
    return 'Done'


def get_user_by_name(first_name: str, second_name: str):
    # cnx = mysql.connector.connect(host="172.20.0.1", user='admin', password='admin', database='dev')
    # cursor = cnx.cursor()
    # with managed_resource() as (cursor, cnx):
    #     cursor.execute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
    #     user_list = []
    #     for (id, first_name, second_name, age, birthdate, biography, city, disabled) in cursor:
    #         user_dict = {}
    #         user_dict["id"] = id[0], 
    #         user_dict["first_name"] = first_name[0], 
    #         user_dict["second_name"] = second_name[0], 
    #         user_dict["age"] = age[0], 
    #         user_dict["birthdate"] = birthdate[0], 
    #         user_dict["biography"] = biography[0], 
    #         user_dict["city"] = city[0], ХЙЦ
    #         user_dict["disabled"] = disabled[0]
    # CREATE INDEX users_search_index ON users (first_name, second_name);
    #         user_list.append(user_dict)
    #     return user_list
    print(first_name)
    print(second_name)
    with connect_to_replica() as (cursor, cnx):
        cursor.execute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
        rows = cursor.fetchall()
        print(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
        print(rows)
        user_list = []
        for (id, first_name, second_name, age, birthdate, biography, city, disabled) in rows:
            user_dict = {}
            user_dict["id"] = id, 
            user_dict["first_name"] = first_name, 
            user_dict["second_name"] = second_name, 
            user_dict["age"] = age, 
            user_dict["birthdate"] = birthdate, 
            user_dict["biography"] = biography, 
            user_dict["city"] = city, 
            user_dict["disabled"] = disabled
            user_list.append(user_dict)
    return user_list


def get_user_by_name_from_tarantool(first_name: str, second_name: str):
    # cnx = mysql.connector.connect(host="172.20.0.1", user='admin', password='admin', database='dev')
    # cursor = cnx.cursor()
    # with managed_resource() as (cursor, cnx):
    #     cursor.exe    cute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
    #     user_list = []
    #     for (id, first_name, second_name, age, birthdate, biography, city, disabled) in cursor:
    #         user_dict = {}
    #         user_dict["id"] = id[0], 
    #         user_dict["first_name"] = first_name[0], 
    #         user_dict["second_name"] = second_name[0], 
    #         user_dict["age"] = age[0], 
    #         user_dict["birthdate"] = birthdate[0], 
    #         user_dict["biography"] = biography[0], 
    #         user_dict["city"] = city[0], ХЙЦ
    #         user_dict["disabled"] = disabled[0]
    # CREATE INDEX users_search_index ON users (first_name, second_name);
    #         user_list.append(user_dict)
    #     return user_list
    print(first_name)
    print(second_name)

    connection = tarantool.connect("mytarantool", 3301)
    # tarantool.connect("mytarantool", 3301, user='guest', password='pass')
    # tester = connection.space('users')
    res = connection.call('myproc', (first_name, second_name))
    print(res)
    user_list = []
    for (id, first_name, second_name, age, birthdate, biography, city, disabled) in res:
        user_dict = {}
        user_dict["id"] = id, 
        user_dict["first_name"] = first_name, 
        user_dict["second_name"] = second_name, 
        user_dict["age"] = age, 
        user_dict["birthdate"] = birthdate, 
        user_dict["biography"] = biography, 
        user_dict["city"] = city, 
        user_dict["disabled"] = disabled
        user_list.append(user_dict)
    return user_list

def get_user_info(id: str):
    # cnx = mysql.connector.connect(host="172.20.0.1", user='admin', password='admin', database='dev')
    # cursor = cnx.cursor()
    with managed_resource() as (cursor, cnx):
        cursor.execute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where id = '{id}' limit 1")
        row = cursor.fetchone()

    user_dict = {}
    if row:
        for v, k in zip(row, ['id', 'first_name', 'second_name', 'age', 'birthdate', 'biography', 'city', 'disabled']):
            user_dict[k] = v
        return User(**user_dict)
    return {}


def get_user(id: str):
    # cnx = mysql.connector.connect(host="172.20.0.1", user='admin', password='admin', database='dev')
    # cursor = cnx.cursor()
    with managed_resource() as (cursor, cnx):
        cursor.execute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled, hashed_password from users where id = '{id}' limit 1")
        row = cursor.fetchone()

    user_dict = {}
    if row:
        for v, k in zip(row, ['id', 'first_name', 'second_name', 'age', 'birthdate', 'biography', 'city', 'disabled', 'hashed_password']):
            user_dict[k] = v
        return UserInDB(**user_dict)
    return {}


def create_user(user_info: UserInDB) -> str:
    # cnx = mysql.connector.connect(host="172.20.0.1", user='admin', password='admin', database='dev')
    # cursor = cnx.cursor()

    insert_stmt = (
    "INSERT INTO users (id, first_name, second_name, age, birthdate, biography, city, disabled, hashed_password) "
    f"VALUES ('{user_info.id}', '{user_info.first_name}', '{user_info.second_name}', '{user_info.age}', '{user_info.birthdate}', '{user_info.biography}', '{user_info.city}', {user_info.disabled}, '{user_info.hashed_password}')"
    )
    logging.info(insert_stmt)
    data = (user_info.id, user_info.first_name, user_info.second_name, user_info.age, user_info.birthdate, user_info.biography, user_info.city, user_info.disabled, user_info.hashed_password)
    answer = ''
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            cnx.commit()
            answer = "User created!"
        except:
            cnx.rollback()
            answer = "User was not created!"

    # cursor.close()
    # cnx.close()

    return answer


def send_message(sender_id: str, reciever_id: str, message: str) -> str:
    ts = int(datetime.now().strftime('%s'))
    insert_stmt = (
    "INSERT INTO messages (sender_id, reciever_id, message, ts)"
    f" VALUES ('{sender_id}', '{reciever_id}', '{message}', {ts})"
    )
    print(insert_stmt)
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            cnx.commit()
            print('success')
        except:
            cnx.rollback()
            print('failure')



def get_messages(sender_id: str, reciever_id: str) -> str:
    with managed_resource() as (cursor, cnx):
        cursor.execute(f"select message from messages where sender_id = '{sender_id}' and reciever_id = '{reciever_id}'")
        rows = cursor.fetchall()

    return rows


def add_friend(user_id: str, user_friend_id: str):
    insert_stmt = (
    "INSERT INTO friends (user_id, user_friend_id)"
    f" VALUES ('{user_id}', '{user_friend_id}')"
    )
    print(insert_stmt)
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            cnx.commit()
            print('success')
        except:
            cnx.rollback()
            print('failure')

def delete_friend(user_id: str, user_friend_id: str):
    insert_stmt = (
    f"delete from friends where user_id = '{user_id}' and user_friend_id = '{user_friend_id}'"
    )
    print(insert_stmt)
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            cnx.commit()
            print('success')
        except:
            cnx.rollback()
            print('failure')

def create_post(user_id: str, post: str):
    ts = int(datetime.now().strftime('%s'))
    insert_stmt = (
    "INSERT INTO posts (user_id, post, ts)"
    f" VALUES ('{user_id}', '{post}', {ts})"
    )
    print(insert_stmt)
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            cnx.commit()
            print('success')
        except:
            cnx.rollback()
            print('failure')

    insert_stmt = f"select user_friend_id from friends where user_id = {user_id};"
    user_list = []
    with managed_resource() as (cursor, cnx):
        try:
            cursor.execute(insert_stmt)
            for (user_friend_id) in cursor:
                user_list.append(user_friend_id[0])
            print('success')
        except:
            print('failure')
            return None
    
    logging.basicConfig()
    url = "amqp://guest:guest@rabbitmq/"
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    for i in user_list:
        exchange = "test"
        queue = i

        # channel.tx_select()
        channel.exchange_declare(exchange, durable=True)
        channel.basic_publish(exchange, queue, str(post).encode("utf-8"), mandatory=True)
        time.sleep(0.5)
        # channel.tx_rollback()
        connection.close()



def feed_post(user_id: str):        
    logging.basicConfig()
    url = "amqp://guest:guest@rabbitmq/"
    params = pika.URLParameters(url)
    params.socket_timeout = 5
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    #установить ограничение на 5 сообщений единовременно
    channel.basic_qos(prefetch_count=5)
    # channel.tx_select()

    exchange = "test"
    queue = "user_id"

    channel.queue_declare(queue, durable=True)
    channel.queue_bind(queue, exchange)
    #здесь можно включить auto_ack для автоматического подтверждения
    channel.basic_consume(queue, on_message_callback=on_message, auto_ack=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    # try:
    #     channel.start_consuming()
    # except KeyboardInterrupt:
    #     channel.stop_consuming()

    return {user_id: posts}


