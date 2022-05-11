from config.default import *

db = {
      'user' : 'baek',
      'password' : 'baekMy123!',
      'host': 'edu.sky100.kr',
      'port' : 20100,
      'database' : 'emo_movie'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

SECRET_KEY = "dev"