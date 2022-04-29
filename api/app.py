import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.users = {}
app.id_count  = 1

@app.route("/sign-up", methods=['POST'])
def sign_up():
  # a = request.form['id']
  # b = request.form['password']
  # return a + b
  new_user = request.json;
  new_user['id'] = app.id_count
  print("----------")
  print(app.id_count)
  print(new_user)
  print(jsonify(new_user))
  print("----------")
  
  app.users[app.id_count] = new_user
  app.id_count = app.id_count+1
  return jsonify(new_user)

@app.route("/ping", methods=['GET'])
def ping():
  return "pong"

@app.route("/", methods=['get','post'])
def main():
  return render_template('main.html')

app.tweets = []

@app.route('/tweet',methods=['POST'])
def tweet():
  payload = request.json
  user_id = int(payload['id'])
  tweet = payload['tweet']
  print(user_id)
  print(tweet)
  if user_id not in app.users:
    return '사용자가 존재하지 않습니다', 400
  if len(tweet) > 300:
    return '300자를 넘었습니다', 400
  
  user_id = int(payload['id'])
  app.tweets.append({
    'user_id' : user_id,
    'tweet' : tweet
  })

  return '', 200