# Candle2

## Pouzite technologie
- Python 3
- MySQL

## Instalacia
1. Vytvor virtual environment v priecinku candle2/
2. Aktivuj virtual environment a nainstaluj don balicky z requirements.txt:
   `python3 -m pip install -r requirements.txt`
   
3. Vytvor subor ".env", do ktoreho vloz 2 riadky:
   `SECRET_KEY=<YOUR_SECRET_KEY>` a 
   `SQLALCHEMY_DATABASE_URI=<YOUR_DATABASE_URI>`
4. `<YOUR_DATABASE_URI>` je v tvare `mysql+pymysql://<DB_USERNAME>:<DB_PASSWORD>@localhost/<DB_NAME>`
   

