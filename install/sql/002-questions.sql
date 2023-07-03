create table questions
(
    question_id INTEGER                             not null
        constraint questions_pk
            primary key autoincrement,
    title       TEXT                                not null,
    categoryId  INTEGER                             not null
        constraint questions_categories_category_id_fk
            references categories,
    remark      TEXT,
    created_at  TIMESTAMP default CURRENT_TIMESTAMP not null,
    updated_at  TIMESTAMP default CURRENT_TIMESTAMP not null
);

