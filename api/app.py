import json
from turtle import pd
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, Text


def create_app(test_config=None):
  app = Flask(__name__)
   
  if test_config is None:
    app.config.from_pyfile("config.py")
  else:
    app.config.update(test_config)

  database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow = 0)
  app.database = database
  
  #main
  @app.route('/')
  def main():
    return render_template('main.html')

  #db 에서 영화 정보 불러오기
  @app.route("/movie/<string:title>",methods=['GET'])
  def movie(title):
    #db에서 데이터 조회 후 json으로 반환
    # objects = app.database.execute(f"select * from movie_info where title = \'{title}\'").fetchall()
    # if len(objects) == 0:
    #   return "not found"
    # objects = objects[0] 
    # print(title)

    # return jsonify({  #db 있을때
    #   'Title' : objects[1],
    #   'Token' :  objects[2], #youtube video id
    #   'TimeStamp' : objects[3],
    #   'Param' : 5  ,  #그래프 좌표 스케일
    #   'Category' : objects[4] ,
    # })

    return jsonify({  #db 없을때
      'Title' : 'moonKnight',
      'Token' : 'GDpE41slO9w', #youtube video id
      'Category' : 'action' ,
      'TimeStamp' : '15,30,45,60',
      'Param' : 5    #그래프 좌표 스케일
    })


  # fetch 로 json 받는 예제
  @app.route("/test")
  def test():
    return render_template('test.html')
  
  @app.route("/sign-up", methods=['POST'])
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



