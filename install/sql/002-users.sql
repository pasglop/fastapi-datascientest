create table users
(
    user_id        integer                             not null
        constraint users_pk
            primary key autoincrement,
    user_name      TEXT                                not null,
    user_email     TEXT                                not null
        constraint users_pk2
            unique,
    user_password  TEXT                                not null,
    is_admin       boolean   default false             not null,
    created_at     TIMESTAMP default CURRENT_TIMESTAMP not null,
    update_at      TIMESTAMP default CURRENT_TIMESTAMP not null,
    last_logged_at TIMESTAMP
);

