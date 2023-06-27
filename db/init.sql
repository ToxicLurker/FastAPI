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
INSERT INTO users values ('friend1', 'john1', 'doe1', NULL, '1990-05-01', 'I love cookies1', 'Moscow1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 0);
INSERT INTO users values ('friend2', 'john2', 'doe2', NULL, '1990-05-01', 'I love cookies2', 'Moscow2', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 0);


COPY users FROM '/new_people.csv' WITH (FORMAT csv);


CREATE TABLE IF NOT EXISTS messages (
    sender_id VARCHAR(100),
    reciever_id VARCHAR(100),
    message VARCHAR(100),
    ts INT
    );


CREATE TABLE IF NOT EXISTS friends (
    user_id VARCHAR(100),
    user_friend_id VARCHAR(100)
    );

INSERT INTO friends values ('friend1', 'friend2');
INSERT INTO friends values ('friend2', 'friend1');
INSERT INTO friends values ('johndoe', 'friend1');

CREATE TABLE IF NOT EXISTS posts (
    user_id VARCHAR(100),
    post VARCHAR(100),
    ts INT
    );