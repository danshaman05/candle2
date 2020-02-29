from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

''' TODO:
1. vypisat z DB nieco (napr. rooms) - OK 
    1.1 trieda Room - namapovana na tabulku room - OK
    1.2 vytvorit dictionaries - podla pomlciek (vid funkcia Candle::groupSortedByDashes )
    

2.  treba template? - pre kazdy kruzok? .. pre kazdy rocnik?
3. trieda Kruzok
3. vypisat tie kruzky...
'''


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

        print("prefix, suffix : " + prefix, suffix)
        if prefix not in d:
            d[prefix] = []
        if prefix == suffix:
            d[prefix].append(suffix)
        else:
            d[prefix].append('-'.join([prefix, suffix]))

    return d




class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('id', db.BIGINT, primary_key=True)
    name = db.Column('name', db.String(30))
    room_type_id = db.Column("room_type_id", db.BIGINT)
    capacity = db.Column("capacity", db.BIGINT)

    def __repr__(self):
        return "<Room %r>" % self.name

rooms = Room.query.all()
rooms_dict = getRoomsSortedByDashes_dict(rooms) #  ucebne su v jednom dictionary rozdelene podla prefixu
print("nieco")
print(rooms_dict)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/about')
def hello_daniel():
    return 'About page!'

if __name__ == '__main__':
    app.run()