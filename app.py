from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)        # TODO osamostatni do triedy napr. DBService

'''
Autor: Daniel Grohol
Candle2 (prototyp). In this prototype I am reading data from MySQL DB and processing them and printing in same format as in old Candle. 
'''



# TODO osamostatni napr. do Models
class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column('name', db.String(30))
    room_type_id = db.Column("room_type_id", db.BIGINT)
    capacity = db.Column("capacity", db.BIGINT)

    def __repr__(self):
        return "<Room %r>" % self.name

#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


# TODO osamostatnit do routes ??
@app.route('/')
def list_all_rooms():
    rooms = Room.query.all()
    rooms_dict = getRoomsSortedByDashes_dict(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('rooms.html', rooms_dict=rooms_dict)



'''
Rozdeli mena miestnosti podla pomlcok do dictionary, kde key je vzdy prefix miestnosti (napr. F1-108 ma prefix F1)
a value su dane pripony ulozene v poli. 
vstup: 
vystup: dictionary <str, list of str>
'''
def getRoomsSortedByDashes_dict(rooms_lst) -> dict:
    d = dict()
    for room in rooms_lst:
        name = room.name

        # there is one empty string in table room (I don't know why)
        if name == " ":
            continue

        dash_position = name.find('-') # finds first occurence

        if (dash_position) == -1:  # name doesnt contains dash
            prefix = suffix = name
        else:
            prefix = name[0 : dash_position]
            suffix = name[dash_position + 1 : ]

        # ak su data v zlom formate:
        # raise Exception("Bad data format for room. Room must be in format 'prefix-suffix', for example: 'F1-208'")

        #xMieRez je specialny pripad:
        if 'xMieRez' in prefix:
            suffix = prefix
            prefix = "Ostatné"
            if prefix not in d:
                d[prefix] = []
            d[prefix].append(suffix)
        else:
            if prefix not in d:
                d[prefix] = []
            if prefix == suffix:
                d[prefix].append(suffix)
            else:
                d[prefix].append('-'.join([prefix, suffix]))

    return d


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



