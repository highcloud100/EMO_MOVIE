from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import create_engine
from datetime import timedelta
from werkzeug.utils import secure_filename


class userInfo():
    def __init__(self,id, username, gender, age, date,email):
        self.id = id
        self.username = username
        self.gender = gender
        self.age = age
        self.date = date
        self.email = email
    def print(self):
        print(self)


def create_app(test_config=None):
  app = Flask(__name__)

  app.config.from_envvar('APP_CONFIG_FILE')
  app.permanent_session_lifetime = timedelta(minutes=60) #세션 만료 시간 1시간
  database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow = 0)
  app.database = database
  
  @app.route('/') # 디폴트 화면
  def login():
    return render_template('sign_up.html')


  #영화 선택하는 화면 
  @app.route('/select')
  def movieSelect():
    if 'user' in session:
      objects = app.database.execute("select title from movie_info").fetchall() #db에서 영화 리스트 뽑아옴
      print(objects)
      return render_template('select.html', mlist=objects, username = session['user']['username']) #home.html에 반환
    else:
       return render_template('sign_up.html')

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

  #정보 입력 페이지
  @app.route('/signup', methods=['GET', 'POST'])
  def signup():
      if request.method=='POST':
          session.clear()
          session.permanent = True

          try:
              # 회원정보 생성
              username = request.form['name']
              gender = request.form['gender']
              age = request.form['age']
              #date = request.form('date')
              email = request.form['email']

              print(username)  # 들어오나 확인
              print(gender)  
              obj = app.database.execute(f"select * from subject_info where name=\'{username}\' and age={age} and email=\'{email}\';").fetchall()
              if len(obj)>0:
                  raise Exception('이미 존재하는 정보입니다')

              app.database.execute(
                  f"INSERT INTO subject_info(name, gender, age, email) VALUES(\'{username}\',\'{gender}\' ,{age},\'{email}\')")

              obj =  app.database.execute(f"select * from subject_info where name=\'{username}\';").fetchone()
              user = userInfo(obj[0], obj[1], obj[2], obj[3],obj[4],obj[5])
              #세션 저장
              session['user'] = user.__dict__
              print(session['user']['username'])

              return redirect(url_for('movieSelect'))
          except Exception as e:
              print(e)
              session.clear()
              
              if(str(e)=='이미 존재하는 정보입니다'):
                  return f"<script>alert('{e}'); location.href='/'</script>"
              else:
                    return f"<script>alert('올바르지 않은 정보'); location.href='/'</script>"
      else:
          session.clear()
          return render_template('sign_up.html')

  #포스터 바꾸는 페이지
  @app.route('/poster')
  def render_file():
    objects = app.database.execute("select title from movie_info").fetchall() #db에서 영화 리스트 뽑아옴
    print(objects)
    return render_template('upload.html',mlist=objects)

  #이미지 업로드
  @app.route('/posterUpload', methods=['GET','POST'])
  def upload_poster():
    if request.method == 'POST' and request.form['pwd'] == "1234":
      f = request.files['file']
      print(app.root_path)
      f.save( app.root_path + '/static/'+ secure_filename(request.form['title']+'.png'))
    return redirect(url_for('render_file'))
  
  @app.route('/logout') #마지막에
  def logout():
    session.clear()
    # session.pop('usernmae', None) 이것도 가능?
    return redirect("/")

  @app.route('/request', methods=['GET', 'POST'])
  def timestamp():
      data = request.get_json()
      white = data['WHITE']
      yellow = data['YELLOW']
      green = data['GREEN']
      title = data['TITLE']
      try:
          
        #하나만
        # x = white[0]
        # print(x)
        # ddate = x.split(":")
        # point = ddate[1].split(", ")
        # print(ddate)
        # print(point)

        #white
        time = []
        point_White_x = []
        point_White_y = []
        for i in range(len(white)):
            x = white[i]
            ddate = x.split(":")
            print(ddate[0])
            point = ddate[1].split(", ")
            print(point)
            time.append(ddate[0])
            point_White_x.append(float(point[0]))
            point_White_y.append(float(point[1]))

        white_x = sum(point_White_x) / (len(white))
        white_y = sum(point_White_y) / (len(white))


        point_Yellow_x = []
        point_Yellow_y = []
        for i in range(len(yellow)):
            x = yellow[i]
            ddate = x.split(":")
            point = ddate[1].split(", ")
            time.append(ddate[0])
            point_Yellow_x.append(float(point[0]))
            point_Yellow_y.append(float(point[1]))

        yellow_x = sum(point_Yellow_x) / (len(yellow))
        yellow_y = sum(point_Yellow_y) / (len(yellow))

        point_Green_x, point_Green_y = [], []
        for i in range(len(green)):
            x = green[i]
            ddate = x.split(":")
            point = ddate[1].split(", ")
            time.append(ddate[0])
            point_Green_x.append(float(point[0]))
            point_Green_y.append(float(point[1]))

        green_x = sum(point_Green_x) / (len(green))
        green_y = sum(point_Green_y) / (len(green))

        # date 제외, 좌표 찍은 시간들은 column 만들어야 할 듯?
        app.database.execute(f"INSERT INTO data(subjectID, movieTitle, white_x, white_y, yellow_x, yellow_y, green_x, green_y) \
        VALUES(\'{session['username']}\', \'{title}\', {str(white_x)}, {str(white_y)}, {str(yellow_x)}, {str(yellow_y)}, {str(green_x)}, {str(green_y)})")
        return redirect(url_for('movieSelect'))
      except:
        print("error")
        return f"<script>alert('error'); location.href='/select'</script>"


  return app



# set FLASK_APP=app
# set FLASK_ENV=development
# set APP_CONFIG_FILE=E:\-\2022-1\인턴십\EMO_MOVIE\EMO_MOVIE\api\config\devel.py

#mysql-connector