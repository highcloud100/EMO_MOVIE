import json
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, Text


def create_app(test_config=None):
  app = Flask(__name__)

  app.config.from_envvar('APP_CONFIG_FILE')

  database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow = 0)
  app.database = database
  
  #영화 선택하는 화면 / 디폴트 화면
  @app.route('/')
  def home():
    objects = app.database.execute("select title from movie_info").fetchall() #db에서 영화 리스트 뽑아옴
    print(objects)
    return render_template('select.html', mlist=objects) #home.html에 반환

  # 영화 요청시 반환
  @app.route('/movie', methods=['POST'])  #home.html에서 영화 선택시 post 
  def movie():
    Title = request.form['title']
    print(Title)
    return render_template('main.html', title = Title) #main.html 에 영화 제목 반환


  #db에서 영화 정보 불러오기
  @app.route("/movie/<string:title>",methods=['GET', 'POST'])
  def getMovie(title):
    #db에서 데이터 조회 후 json으로 반환
    objects = app.database.execute(f"select * from movie_info where title = \'{title}\'").fetchall()
    if len(objects) == 0:
      return "not found"
    objects = objects[0] 

    print(title)

    return jsonify({  #db 있을때
      'Title' : objects[1],
      'Token' :  objects[2], #youtube video id
      'TimeStamp' : objects[3],
      'Param' : 5  ,  #그래프 좌표 스케일
      'Category' : objects[4] ,
    })


  # fetch 로 json 받는 예제
  @app.route("/test")
  def test():
    return render_template('test.html')
  
  @app.route("/sign-up", methods=['GET','POST'])
  def sign_up():
    # a = request.form['id']
    # b = request.form['password']
    # return a + b
    new_user = request.json;

    print("--- 받은 정보 -------")
    print(new_user)
    print(jsonify(new_user))
    print("---------------------")

    return jsonify(new_user)

  return app



# set FLASK_APP=pybo
# set FLASK_ENV=development
# set APP_CONFIG_FILE=C:\PROJECT\EMO_MOVIE\api\config\devel.py