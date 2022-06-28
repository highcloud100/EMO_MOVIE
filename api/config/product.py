db = {
      'user' : 'emo',
      'password' : 'EMOmovie123!',
      'host': '165.246.141.212',
      'port' : 20100,
      'database' : 'emo_db'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?auth_plugin=mysql_native_password&charset=utf8"


SECRET_KEY = b'\xd1]0 CV\x9a\rB`}\x98\xa2z3\xca'