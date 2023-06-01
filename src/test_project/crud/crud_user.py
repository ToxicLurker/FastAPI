import mysql
from ..models.user_models import UserInDB, User
from contextlib import contextmanager
import mysql.connector
import logging

@contextmanager
def managed_resource():
    cnx = mysql.connector.connect(host="172.19.0.1", user='admin', password='admin', database='dev')
    cursor = cnx.cursor()
    try:
        yield (cursor, cnx)
    finally:
        cursor.close()
        cnx.close()


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
    cnx = mysql.connector.connect(host="172.19.0.1", user='admin', password='admin', database='dev')
    cursor = cnx.cursor()
    cursor.execute(f"select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
    user_list = []
    for (id, first_name, second_name, age, birthdate, biography, city, disabled) in cursor:
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
    cursor.close()
    cnx.close()
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


def show_index(first_name: str, second_name: str):
    cnx = mysql.connector.connect(host="172.19.0.1", user='admin', password='admin', database='dev')
    cursor = cnx.cursor()
    cursor.execute(f"explain select id, first_name, second_name, age, birthdate, biography, city, disabled from users where first_name like '{first_name}%' and second_name like '{second_name}%' order by id")
    row = cursor.fetchone()
    logging.info("explain")
    logging.info(row)
    print("explain")
    print(row)
    cursor.close()
    cnx.close()
    return row