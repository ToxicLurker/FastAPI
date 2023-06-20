-- CREATE DATABASE dev;
-- CREATE DATABASE test;

create role replicator with login replication password 'pass';

\c dev;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(100),
    first_name VARCHAR(100),
    second_name VARCHAR(100),
    age VARCHAR(100) NULL,
    birthdate VARCHAR(100) NULL,
    biography VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    hashed_password VARCHAR(100),
    disabled INT
    );

INSERT INTO users values ('johndoe', 'john', 'doe', NULL, '1990-05-01', 'I love cookies', 'Moscow', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 0);


COPY users FROM '/new_people.csv' WITH (FORMAT csv);


CREATE TABLE IF NOT EXISTS messages (
    sender_id VARCHAR(100),
    reciever_id VARCHAR(100),
    message VARCHAR(100),
    ts INT
    );