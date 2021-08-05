CREATE TABLE IF NOT EXISTS users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    adding_date   timestamp,
    id        serial            not null
);

alter table users
    owner to postgres;

create unique index IF NOT EXISTS users_id_index
    on users (id);

CREATE TABLE IF NOT EXISTS messages
(
    id              serial              primary key,
    message_id      bigint              not null,
    chat_id         bigint              not null
);