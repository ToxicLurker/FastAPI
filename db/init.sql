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
-- LOAD DATA INFILE '/var/lib/mysql-files/new_people.csv' 
-- INTO TABLE users 
-- CHARACTER SET utf8
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;


-- CREATE TABLE IF NOT EXISTS users1 (
--     fullname TEXT,
--     age TEXT NULL,
--     city TEXT NULL
--     ) ENGINE=InnoDB CHARACTER SET=utf8;



-- LOAD DATA INFILE '/var/lib/mysql-files/people.csv' 
-- INTO TABLE users1 
-- CHARACTER SET utf8
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
