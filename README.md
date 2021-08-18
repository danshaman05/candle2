# Candle (New generation)

***IMPORTANT: This readme file is not finished yet.***



## Requirements
- Python 3.5
- MySQL

## Install & Run (Linux)


Clone the repository and install Python Virtual Environment in it:
```commandline
git clone https://github.com/fmfi-svt/candle-ng.git
cd candle-ng
python3 -m venv venv
```

Activate the environment and install dependencies:
```commandline
$ source venv/bin/activate
(venv) $ python3 -m pip install -r requirements/requirements.txt
```

During development, install `requirements/dev_requirements.txt`

Generate a Flask Secret key. It's easy with Python:
```python
>>> import secrets
>>> secrets.token_urlsafe(16)
```

Setup a MySQL database with corresponding tables (check [DB model diagram](diagrams/db_model.png)). 
Email us at <fmfi-svt@googlegroups.com> and we will send you a MySQL dump-file 
from old Candle instance you can work with. 


Create a file called ".env" in the root folder (candle-ng/) and save here these configuration values:
```commandline
FLASK_APP=run.py
FLASK_ENV=YOUR_ENVIRONMENT_GOES_HERE
SECRET_KEY=YOUR_SECRET_KEY_GOES_HERE 
SQLALCHEMY_DATABASE_URI=YOUR_DATABASE_URI_GOES_HERE
```
1. Replace `YOUR_ENVIRONMENT_GOES_HERE` with `development` or `production`.
2. Replace `YOUR_SECRET_KEY_GOES_HERE` with your secret key.
3. Replace `YOUR_DATABASE_URI_GOES_HERE` with your database URI, for example: `mysql+pymysql://username:password@server/db`.


Run the app:
```commandline
(venv) $ flask run
```