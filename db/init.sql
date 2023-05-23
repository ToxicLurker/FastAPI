CREATE DATABASE IF NOT EXISTS dev;
CREATE DATABASE IF NOT EXISTS test;
USE dev;
CREATE TABLE IF NOT EXISTS users (
    id TEXT,
    first_name TEXT,
    second_name TEXT,
    age TEXT NULL,
    birthdate TEXT NULL,
    biography TEXT NULL,
    city TEXT NULL,
    hashed_password TEXT,
    disabled TINYINT
    ) ENGINE=InnoDB CHARACTER SET=utf8;

INSERT INTO users values("johndoe", "john", "doe", NULL, '1990-05-01', "I love cookies", "Moscow", "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", 0);

LOAD DATA INFILE '/var/lib/mysql-files/new_people.csv' 
INTO TABLE users 
CHARACTER SET utf8
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


CREATE TABLE IF NOT EXISTS users1 (
    fullname TEXT,
    age TEXT NULL,
    city TEXT NULL
    ) ENGINE=InnoDB CHARACTER SET=utf8;



LOAD DATA INFILE '/var/lib/mysql-files/people.csv' 
INTO TABLE users1 
CHARACTER SET utf8
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
