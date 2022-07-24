from logging.config import dictConfig
import os


db = {
      'user' : 'emo',
      'password' : 'EMOmovie123!',
      'host': '165.246.141.212',
      'port' : 20100,
      'database' : 'emo_db'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?auth_plugin=mysql_native_password&charset=utf8"


SECRET_KEY = b'\xd1]0 CV\x9a\rB`}\x98\xa2z3\xca'


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':'/home/affctiv/projects/EMO_MOVIE/api/logs/logfile.log' ,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
