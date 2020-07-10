from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'    # Kvoli collation - zatial nevyuzivame.
db = SQLAlchemy(app)

# icu zatial nevyuzivam, kedze neviem sortovat podla priezviska a mena ucitela zaroven:
import icu  # pre spravne sortovanie ucitelov, miestnosti, kruzkov v SK jazyku
icu_collator = icu.Collator.createInstance(icu.Locale('sk_SK.UTF-8'))

from candle_backend import routes