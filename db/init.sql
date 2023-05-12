CREATE DATABASE IF NOT EXISTS dev;
CREATE DATABASE IF NOT EXISTS test;
USE dev;
CREATE TABLE IF NOT EXISTS users (
    id TEXT,
    first_name TEXT,
    second_name TEXT,
    age TEXT,
    birthdate TEXT,
    biography TEXT,
    city TEXT,
    hashed_password TEXT,
    disabled TINYINT
    );

INSERT INTO users values("johndoe", "john", "doe", null, '1990-05-01', "I love cookies", "Moscow", "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", 0);
