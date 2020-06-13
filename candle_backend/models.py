from candle_backend import db

# TODO Treba popridavat nullable=False, db.ForeignKey k atributom

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column('name', db.String(30))
    room_type_id = db.Column("room_type_id", db.BIGINT)  # treba nastavit cudzi kluc?
    capacity = db.Column("capacity", db.BIGINT)

    def __repr__(self):
        return "<Room %r>" % self.name



class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column('id', db.BIGINT, primary_key=True)
    day = db.Column('day',db.BIGINT)
    start = db.Column("start", db.BIGINT)
    end = db.Column("end", db.BIGINT)
    lesson_type_id = db.Column("lesson_type_id", db.BIGINT, db.ForeignKey('lesson_type.id'))  # treba nastavit cudzi kluc?
    room_id = db.Column("room_id", db.BIGINT)
    subject_id = db.Column("subject_id", db.BIGINT)
    external_id = db.Column("external_id", db.BIGINT)
    note = db.Column("note", db.VARCHAR)


    def __repr__(self):
        return f"Lesson(id:'{self.id}', room_id:'{self.room_id}' )"


    def getDayAbbreviation(self) -> str:
        '''Vrati skratku dna v tyzdni.'''

        days = ['Po', 'Ut', 'St', 'Št', 'Pi']
        return days[self.day]


    def getListOfTeachers(self):
        '''Vrati zoznam ucitelov'''




class LessonType(db.Model):
    __tablename__ = 'lesson_type'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column("name", db.VARCHAR)
    code = db.Column("code", db.VARCHAR)

    def __repr__(self):
        return f"{self.name}"



class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column("name", db.VARCHAR)
    code = db.Column("code", db.VARCHAR)
    short_code = db.Column("short_code", db.VARCHAR)
    credit_value = db.Column('credit_value', db.BIGINT)
    rozsah = db.Column('rozsah', db.VARCHAR)
    external_id = db.Column('external_id', db.VARCHAR)

    def __repr__(self):
        return f"Subject(id:'{self.id}', name:'{self.name}' )"



class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column('id', db.BIGINT, primary_key=True)
    given_name = db.Column("given_name", db.VARCHAR)
    family_name = db.Column("family_name", db.VARCHAR)
    iniciala = db.Column("iniciala", db.VARCHAR)

    oddelenie = db.Column("oddelenie", db.VARCHAR)
    katedra = db.Column("katedra", db.VARCHAR)
    eternal_id = db.Column("external_id", db.VARCHAR)
    login = db.Column("login", db.VARCHAR)
    slug = db.Column("slug", db.VARCHAR)

    def __repr__(self):
        return f"Teacher(id:'{self.id}', given_name:'{self.given_name}' )"



class Teacher_lessons(db.Model):
    __tablename__ = 'teacher_lessons'
    id = db.Column('id', db.BIGINT, primary_key=True)
    teacher_id = db.Column('teacher_id', db.BIGINT, db.ForeignKey('teacher.id'))
    lesson_id = db.Column('lesson_id', db.BIGINT, db.ForeignKey('lesson.id'))