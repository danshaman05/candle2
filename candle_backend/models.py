from candle_backend import db


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column('name', db.String(30))
    room_type_id = db.Column("room_type_id", db.BIGINT)
    capacity = db.Column("capacity", db.BIGINT)

    def __repr__(self):
        return "<Room %r>" % self.name

