from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/about')
def hello_daniel():
    return 'About page!'

if __name__ == '__main__':
    app.run()
