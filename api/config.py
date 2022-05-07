db = {
  'user' : 'movie',
  'password' : 'emo123movie?',
  'host': 'localhost',
  'port' : 3306,
  'database' : 'emo_movie'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"