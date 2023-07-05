create table answers
(
    answer_id   integer
        constraint answers_pk
            primary key autoincrement,
    question_id integer                             not null,
    answer_text TEXT                                not null,
    is_correct  boolean   default false             not null,
    created_at  TIMESTAMP default CURRENT_TIMESTAMP not null,
    updated_at  TIMESTAMP default CURRENT_TIMESTAMP not null,
  CONSTRAINT fk_questions
    FOREIGN KEY (question_id)
    REFERENCES questions(question_id)
    ON DELETE CASCADE
);

