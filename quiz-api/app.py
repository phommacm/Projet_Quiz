import sqlite3
from flask import Flask, request
from flask_cors import CORS

import hashlib

from jwt_utils import build_token

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	tried_password = payload['password'].encode('UTF-8')
	hashed = hashlib.md5(tried_password).digest()

	if (hashed == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'):
		return {"token": build_token()}, 200
	else:
		return "Unauthorized", 401

@app.route('/questions', methods=['POST'])
def PostAddQuestion():
    question_data = request.get_json()
    
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quiz_questions (position, title, text, image) VALUES (?, ?, ?, ?)",
                   (question_data['position'], question_data['title'], question_data['text'], question_data['image']))
    question_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {"question_id": question_id}, 200

if __name__ == "__main__":	
    app.run()
    