import json, pymysql
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, text

def create_app(test_config = None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0) # db connect
    app.database = database # create 함수 외부에서 db 사용할 수 있도록

    @app.route('/')
    def main():
        return render_template('front.html')

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user_id = app.database.execute(text("""
            Insert INTO subject_Info(
                KeyName,
                Gender,
                Age,
                Date
            ) VALUES (
                :KeyName,
                :Gender,
                :Age,
                :Date
            )
        """), new_user).lastrowid

        row = app.database.execute(text("""
            SELECT
                KeyName,
                Gender,
                Age,
                Date
            FROM subject_Info
            WHERE id = :user_id
        """), {
            'user_id' : new_user_id
        }).fetchone()

        created_user = {
            'KeyName': row['KeyName'],
            'Gender': row['Gender'],
            'Age': row['Age'],
            'Date': row['Date']
        } if row else None
        return jsonify(created_user)


    @app.route("/movie/<string:title>", methods=['GET'])
    def movie(title):
        objects = app.database.execute(f"select * from movie_info where title = \'{title}\'").fetchall()
        if len(objects) == 0:
          return "not found"
        objects = objects[0]
        print(title)

        return jsonify({
          'Title': objects[1],
          'YoutubeToken':  objects[2],
          'TimeString': objects[3],
          'Category': objects[4]
        })

    # @app.route("/result", methods=['POST'])
    # def result():

    return app
