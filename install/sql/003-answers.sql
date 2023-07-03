create table answers
(
    answer_id   integer
        constraint answers_pk
            primary key autoincrement,
    question_id integer                             not null
        constraint answers_questions_question_id_fk
            references questions,
    answer_text TEXT                                not null,
    is_correct  boolean default false not null,
    created_at  TIMESTAMP default CURRENT_TIMESTAMP not null,
    updated_at  TIMESTAMP default CURRENT_TIMESTAMP not null
);

