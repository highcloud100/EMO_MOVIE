from config.default import *

db = {
      'user' : 'emo',
      'password' : 'EMOmovie123!',
      'host': '165.246.141.212',
      'port' : 20100,
      'database' : 'emo_db'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

SECRET_KEY = "dev"