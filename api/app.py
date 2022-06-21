from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import create_engine
from datetime import timedelta
from werkzeug.utils import secure_filename

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
    if 'username' in session:
      objects = app.database.execute("select title from movie_info").fetchall() #db에서 영화 리스트 뽑아옴
      print(objects)
      return render_template('select.html', mlist=objects, username = session['username']) #home.html에 반환
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

  @app.route('/signup', methods=['GET', 'POST'])
  def signup():
    if request.method=='POST':
        session.clear()
        session.permanent = True
        session['username'] = request.form['name']
        # 회원정보 생성
        username = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        #date = request.form('date')
        email = request.form['email']

        print(username)  # 들어오나 확인
        print(gender)  

        app.database.execute(
            #f"INSERT INTO subject_info(name, gender, age, date, email) VALUES({userInfo.username}, {userInfo.gender}, {userInfo.age}, {userInfo.date}, {userInfo.email})")
            f"INSERT INTO subject_info(name, gender, age) VALUES(\'{username}\',\'{gender}\' ,{age})")
        return redirect(url_for('movieSelect'))
    else:
      session.clear()
      return render_template('sign_up.html')

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
      print(app.root_path);
      f.save( app.root_path + '/static/'+ secure_filename(request.form['title']+'.png'))
    return redirect(url_for('render_file'))
  return app



# set FLASK_APP=pybo
# set FLASK_ENV=development
# set APP_CONFIG_FILE=C:\PROJECT\EMO_MOVIE\api\config\devel.py