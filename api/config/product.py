db = {
      'user' : 'baek',
      'password' : 'baekMy123!',
      'host': 'edu.sky100.kr',
      'port' : 20100,
      'database' : 'emo_movie'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?auth_plugin=mysql_native_password&charset=utf8"


SECRET_KEY = b'\xd1]0 CV\x9a\rB`}\x98\xa2z3\xca'