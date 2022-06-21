from flask_sqlalchemy import SQLAlchemy
from flask import app
from datetime import timedelta, datetime
from flask import render_template
import json
from turtle import pd
from sqlalchemy import create_engine, Text
from flask import Flask, render_template, redirect, request, session, jsonify, url_for
from flask_session import Session


class userInfo():
    def __init__(self, username, gender, age, date):
        self.username = username
        self.gender = gender
        self.age = age
        self.date = date

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = '0000' # secret_key는 서버상에 동작하는 어플리케이션 구분하기 위해 사용하고 복잡하게 만들어야함.
    #session(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    @app.route('/')
    def login():
        return render_template('signup.html')

    @app.route('/signup', methods=['POST'])
    def signup():
        session.clear()

        #######################

        username = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        # date = request.form('date')
        email = request.form['email']

        try:
            data = userInfo.query.filter_by(username=username, email=email).first()
            if data is not None:
                session['username'] = request.form['name']
                app.database.execute(
                    # f"INSERT INTO subject_info(name, gender, age, date, email) VALUES({userInfo.username}, {userInfo.gender}, {userInfo.age}, {userInfo.date}, {userInfo.email})")
                    f"INSERT INTO subject_info(name, age) VALUES(\'{username}\', {age})")
                return redirect(url_for('movieSelect'))
            else:
                return 'Don\'t Login'
        except:
            return "Don't Login"

        #######################
        # 기존 Version(예외처리 전)
        # session['username'] = request.form['name']
        # # 회원정보 생성
        # username = request.form['name']
        # gender = request.form['gender']
        # age = request.form['age']
        # # date = request.form('date')
        # email = request.form['email']
        #
        # print(username)  # 들어오나 확인
        #
        # app.database.execute(
        #     # f"INSERT INTO subject_info(name, gender, age, date, email) VALUES({userInfo.username}, {userInfo.gender}, {userInfo.age}, {userInfo.date}, {userInfo.email})")
        #     f"INSERT INTO subject_info(name, age) VALUES(\'{username}\', {age})")
        # return redirect(url_for('movieSelect'))
        ############################

    # 영화 선택하는 화면
    @app.route('/select')
    def movieSelect():
        objects = app.database.execute("select title from movie_info").fetchall()  # db에서 영화 리스트 뽑아옴
        print(objects)
        return render_template('select.html', mlist=objects)  # home.html에 반환

    # 영화 요청시 반환
    @app.route('/movie', methods=['POST'])  # home.html에서 영화 선택시 post
    def movie():
        Title = request.form['title']
        print(Title)
        return render_template('main.html', title=Title)  # main.html 에 영화 제목 반환

    # db에서 영화 정보 불러오기
    @app.route("/movie/<string:title>", methods=['GET', 'POST'])
    def getMovie(title):
            # # db에서 데이터 조회 후 json으로 반환
          objects = app.database.execute(f"select * from movie_info where title = \'{title}\'").fetchall()
          if len(objects) == 0:
            return "not found"
          objects = objects[0]
          print(title)
          return jsonify({  # db 있을때
              'Title': objects[1],
              'Token': objects[2],  # youtube video id
              'TimeStamp': objects[3],
              'Param': 5,  # 그래프 좌표 스케일
              'Category': objects[4],
          })

    @app.route('/request', methods=['GET', 'POST'])
    def timestamp():
        data = request.get_json()
        white = data['WHITE']
        yellow = data['YELLOW']
        green = data['GREEN']

        #하나만
        # x = white[0]
        # print(x)
        # ddate = x.split(":")
        # point = ddate[1].split(", ")
        # print(ddate)
        # print(point)

        #white
        time = [], point_White_x = [], point_White_y = []
        for i in range(len(white)):
            x = white[i]
            ddate = x.split(":")
            point = ddate[1].split(", ")
            time += ddate[0]
            point_White_x += point[0]
            point_White_y += point[1]

        point_Yellow_x = [], point_Yellow_y = []
        for i in range(len(yellow)):
            x = yellow[i]
            ddate = x.split(":")
            point = ddate[1].split(", ")
            time += ddate[0]
            point_Yellow_x += point[0]
            point_Yellow_y += point[1]

        point_Green_x = [], point_Green_y = []
        for i in range(len(green)):
            x = green[i]
            ddate = x.split(":")
            point = ddate[1].split(", ")
            time += ddate[0]
            point_Green_x += point[0]
            point_Green_y += point[1]


        app.database.execute(f"SELECT * FROM LEFT JOIN subject_info ON data.subjectID = subject_info.id")
        app.database.execute(f"SELECT * FROM LEFT JOIN movie_info ON data.movieTitle = movie_info.title")

        #subjectID, movieTitle 못함
        app.database.execute(f"INSERT INTO data(date, subjectID, movieTitle, white_x, white_y, yellow_x, yellow_y, green_x, green_y) \
                            VALUES(\'{time}\', {}, {}, {point_White_x}, {point_White_y}, {point_Yellow_x}, {point_Yellow_y}, {point_Green_x}, {point_Green_y})") # {} 부분은 추가해야될 부분
        return 'ok'


    @app.route('/logout') #마지막에
    def logout():
        Session["username"] = None
        # session.pop('usernmae', None) 이것도 가능?

        return redirect("/")

    return app













