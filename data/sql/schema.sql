-- Author: Martin Sucha 
CREATE TABLE data_update
  (
     id              BIGINT auto_increment,
     datetime        DATETIME NOT NULL,
     description     VARCHAR(255) NOT NULL,
     version         DATETIME NOT NULL,
     semester        VARCHAR(20) NOT NULL,
     school_year_low BIGINT NOT NULL,
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE free_room_interval
  (
     id      BIGINT auto_increment,
     day     BIGINT NOT NULL,
     start   BIGINT NOT NULL,
     end     BIGINT NOT NULL,
     room_id BIGINT NOT NULL,
     INDEX room_id_idx (room_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE lesson
  (
     id             BIGINT auto_increment,
     day            BIGINT NOT NULL,
     start          BIGINT NOT NULL,
     end            BIGINT NOT NULL,
     lesson_type_id BIGINT NOT NULL,
     room_id        BIGINT NOT NULL,
     subject_id     BIGINT NOT NULL,
     external_id    BIGINT,
     note           VARCHAR(240),
     UNIQUE INDEX external_id_index_idx (external_id),
     INDEX lesson_type_id_idx (lesson_type_id),
     INDEX room_id_idx (room_id),
     INDEX subject_id_idx (subject_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE lesson_type
  (
     id   BIGINT auto_increment,
     name VARCHAR(30) NOT NULL,
     code VARCHAR(1) NOT NULL,
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE linked_lessons
  (
     lesson1_id BIGINT,
     lesson2_id BIGINT,
     PRIMARY KEY(lesson1_id, lesson2_id)
  )
engine = innodb;

CREATE TABLE room
  (
     id           BIGINT auto_increment,
     name         VARCHAR(30) NOT NULL,
     room_type_id BIGINT NOT NULL,
     capacity     BIGINT NOT NULL,
     UNIQUE INDEX external_id_index_idx (name),
     UNIQUE INDEX name_index_idx (name),
     INDEX room_type_id_idx (room_type_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE room_type
  (
     id   BIGINT auto_increment,
     name VARCHAR(30) NOT NULL,
     code VARCHAR(1) NOT NULL,
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE student_group
  (
     id   BIGINT auto_increment,
     name VARCHAR(30) NOT NULL,
     UNIQUE INDEX name_index_idx (name),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE student_group_lessons
  (
     student_group_id BIGINT,
     lesson_id        BIGINT,
     PRIMARY KEY(student_group_id, lesson_id)
  )
engine = innodb;

CREATE TABLE subject
  (
     id           BIGINT auto_increment,
     name         VARCHAR(100) NOT NULL,
     code         VARCHAR(50) NOT NULL,
     short_code   VARCHAR(20) NOT NULL,
     credit_value BIGINT NOT NULL,
     rozsah       VARCHAR(30),
     external_id  VARCHAR(30),
     UNIQUE INDEX external_id_index_idx (external_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE teacher
  (
     id          BIGINT auto_increment,
     given_name  VARCHAR(50),
     family_name VARCHAR(50) NOT NULL,
     iniciala    VARCHAR(50),
     oddelenie   VARCHAR(50),
     katedra     VARCHAR(50),
     external_id VARCHAR(30),
     login       VARCHAR(50),
     slug        VARCHAR(100),
     UNIQUE INDEX login_index_idx (login),
     UNIQUE INDEX slug_index_idx (slug),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE teacher_lessons
  (
     id         BIGINT auto_increment,
     teacher_id BIGINT NOT NULL,
     lesson_id  BIGINT NOT NULL,
     INDEX teacher_id_idx (teacher_id),
     INDEX lesson_id_idx (lesson_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE user
  (
     id    INT auto_increment,
     login VARCHAR(50) NOT NULL UNIQUE,
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE user_timetable
  (
     id        BIGINT auto_increment,
     name      VARCHAR(50) NOT NULL,
     published TINYINT(1) NOT NULL,
     slug      VARCHAR(30),
     user_id   INT NOT NULL,
     UNIQUE INDEX slug_unique_index_idx (slug),
     INDEX user_id_idx (user_id),
     PRIMARY KEY(id)
  )
engine = innodb;

CREATE TABLE user_timetable_lessons
  (
     id                BIGINT auto_increment,
     user_timetable_id BIGINT NOT NULL,
     lesson_id         BIGINT NOT NULL,
     highlighted       TINYINT(1) NOT NULL,
     INDEX user_timetable_id_idx (user_timetable_id),
     INDEX lesson_id_idx (lesson_id),
     PRIMARY KEY(id)
  )
engine = innodb;

ALTER TABLE free_room_interval
  ADD CONSTRAINT free_room_interval_room_id_room_id FOREIGN KEY (room_id)
  REFERENCES room(id);

ALTER TABLE lesson
  ADD CONSTRAINT lesson_subject_id_subject_id FOREIGN KEY (subject_id)
  REFERENCES subject(id) ON DELETE CASCADE;

ALTER TABLE lesson
  ADD CONSTRAINT lesson_room_id_room_id FOREIGN KEY (room_id) REFERENCES room(id
  );

ALTER TABLE lesson
  ADD CONSTRAINT lesson_lesson_type_id_lesson_type_id FOREIGN KEY (
  lesson_type_id) REFERENCES lesson_type(id);

ALTER TABLE linked_lessons
  ADD CONSTRAINT linked_lessons_lesson2_id_lesson_id FOREIGN KEY (lesson2_id)
  REFERENCES lesson(id) ON DELETE CASCADE;

ALTER TABLE linked_lessons
  ADD CONSTRAINT linked_lessons_lesson1_id_lesson_id FOREIGN KEY (lesson1_id)
  REFERENCES lesson(id) ON DELETE CASCADE;

ALTER TABLE room
  ADD CONSTRAINT room_room_type_id_room_type_id FOREIGN KEY (room_type_id)
  REFERENCES room_type(id);

ALTER TABLE student_group_lessons
  ADD CONSTRAINT student_group_lessons_student_group_id_student_group_id FOREIGN
  KEY (student_group_id) REFERENCES student_group(id) ON DELETE CASCADE;

ALTER TABLE student_group_lessons
  ADD CONSTRAINT student_group_lessons_lesson_id_lesson_id FOREIGN KEY (
  lesson_id) REFERENCES lesson(id) ON DELETE CASCADE;

ALTER TABLE teacher_lessons
  ADD CONSTRAINT teacher_lessons_teacher_id_teacher_id FOREIGN KEY (teacher_id)
  REFERENCES teacher(id) ON DELETE CASCADE;

ALTER TABLE teacher_lessons
  ADD CONSTRAINT teacher_lessons_lesson_id_lesson_id FOREIGN KEY (lesson_id)
  REFERENCES lesson(id) ON DELETE CASCADE;

ALTER TABLE user_timetable
  ADD CONSTRAINT user_timetable_user_id_user_id FOREIGN KEY (user_id) REFERENCES
  user(id) ON DELETE CASCADE;

ALTER TABLE user_timetable_lessons
  ADD CONSTRAINT user_timetable_lessons_user_timetable_id_user_timetable_id
  FOREIGN KEY (user_timetable_id) REFERENCES user_timetable(id) ON DELETE
  CASCADE;

ALTER TABLE user_timetable_lessons
  ADD CONSTRAINT user_timetable_lessons_lesson_id_lesson_id FOREIGN KEY (
  lesson_id) REFERENCES lesson(id) ON DELETE CASCADE;
