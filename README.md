# Candle NG

***IMPORTANT: This readme file is not finished yet.***



## Requirements
- Python 3
- MySQL

## Installation (Linux)


Clone the repository and install Python Virtual Environment in it:
```commandline
git clone https://github.com/fmfi-svt/candle-ng.git
cd candle-ng
python3 -m venv venv
```

Activate the environment and install dependencies:
```commandline
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Generate a Flask Secret key. It's easy with Python:
```python
>>> import secrets
>>> secrets.token_urlsafe(16)
```

Setup a MySQL database with corresponding tables (check [DB model diagram](db_model.png)). 
Email us at <fmfi-svt@googlegroups.com> and we will send you a MySQL dump-file 
from old Candle instance you can work with. 

Create a file called ".env" in the root folder (candle-ng/) and save here these two configuration values:
```commandline
SECRET_KEY=YOUR_SECRET_KEY_GOES_HERE 
SQLALCHEMY_DATABASE_URI=YOUR_DATABASE_URI_GOES_HERE
```

(Example of DATABASE_URI: `mysql+pymysql://username:password@server/db`)
