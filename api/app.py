import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.users = {}
app.id_count  = 1

@app.route('/')
def main():
  return render_template('main.html')

@app.route("/movie/<string:title>",methods=['GET'])
def movie(title):

   #db에서 데이터 조회 후 json으로 반환
  print(title)

  return jsonify({
    'Title' : 'moonKnight',
    'Token' : 'GDpE41slO9w', #youtube video id
    'Category' : 'action' ,
    'TimeStamp' : '15,30,45,60',
    'Param' : 5    #그래프 좌표 스케일
  })


