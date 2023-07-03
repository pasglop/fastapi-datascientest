create table questions
(
    question_id INTEGER                             not null
        constraint questions_pk
            primary key autoincrement
        constraint questions_subject_subjects_id_fk
            references subjects,
    title       TEXT                                not null,
    category_id  INTEGER                             not null
        constraint questions_categories_category_id_fk
            references categories,
    subject_id  INTEGER                             not null
        constraint questions_subjects_subject_id_fk
            references categories,
    remark      TEXT,
    created_at  TIMESTAMP default CURRENT_TIMESTAMP not null,
    updated_at  TIMESTAMP default CURRENT_TIMESTAMP not null
);

