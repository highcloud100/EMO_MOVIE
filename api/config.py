from sqlalchemy import create_engine, text

# db = {
#     'host' : 'localhost',
#     'user' : 'root',
#     'password' : '0000',
#     'port' : '3306',
#     'database' : 'mypractice'}
# DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"


db = {
    'user': 'baek',
    'password': 'baekMy123!',
    'host': 'edu.sky100.kr',
    'port': 20100,
    'database': 'emo_movie'
    }


DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

