create table user_answers
(
    user_answer_id integer                             not null
        constraint user_answers_pk
            primary key autoincrement,
    question_id    integer                             not null
        constraint user_answers_questions_question_id_fk
            references questions,
    answer_id      integer                             not null
        constraint user_answers_answers_answer_id_fk
            references answers,
    user_id        integer                             not null
        constraint user_answers_users_user_id_fk
            references users,
    created_at     TIMESTAMP default CURRENT_TIMESTAMP not null
);

