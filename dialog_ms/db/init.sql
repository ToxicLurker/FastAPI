-- CREATE DATABASE dev;
-- CREATE DATABASE test;

create role replicator with login replication password 'pass';

\c dev;


CREATE TABLE IF NOT EXISTS messages (
    sender_id VARCHAR(100),
    reciever_id VARCHAR(100),
    message VARCHAR(100),
    ts INT
    );

