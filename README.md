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

Generate Flask Secret key with python:
```python
>>> import secrets
>>> secrets.token_urlsafe(16)
```

In the "candle" folder create a file called ".env" and save these 2 environment variables in it:
```python
SECRET_KEY=YOUR_SECRET_KEY_GOES_HERE 
SQLALCHEMY_DATABASE_URI=YOUR_DATABASE_URI_GOES_HERE
```

Example of DATABASE_URI: `mysql+pymysql://username:password@server/db`

