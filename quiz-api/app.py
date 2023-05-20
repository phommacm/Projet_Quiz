import sqlite3
from flask import Flask, request
from flask_cors import CORS

import hashlib

from jwt_utils import build_token, decode_token, JwtError

app = Flask(__name__)
CORS(app)

# Endpoint pour tester l'application
@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

# Endpoint pour obtenir des informations sur le quiz
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

# Endpoint pour gérer la connexion
@app.route('/login', methods=['POST'])
def PostLogin():
	payload = request.get_json()
	tried_password = payload['password'].encode('UTF-8')
	hashed = hashlib.md5(tried_password).digest()

	# Renvoie du jeton dans le cas où le mot de passe est correct
	if (hashed == b'\xd8\x17\x06PG\x92\x93\xc1.\x02\x01\xe5\xfd\xf4_@'):
		return {"token": build_token()}, 200
	else:
		return "Unauthorized", 401

# Endpoint pour ajouter une question
@app.route('/questions', methods=['POST'])
def PostAddQuestion():
    # Récupération des données de la question envoyées dans le corps de la requête JSON
    question_data = request.get_json()
    
    # Vérification de l'authentification
    auth_header = request.headers.get('Authorization')
    if (auth_header != None):
        auth_token = auth_header.split(" ")[1]
        try:
            user_id = decode_token(auth_token)
            if user_id == 'quiz-app-admin':
                pass
            else:
                return "Unauthorized", 401
        except JwtError:
            return "Unauthorized", 401
    else:
        return "Unauthorized", 401

	# Insertion de la question dans la base de données
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quiz_questions (position, title, text, image) VALUES (?, ?, ?, ?)",
                   (question_data['position'], question_data['title'], question_data['text'], question_data['image']))
    
	# Récupération de l'identifiant de la question que l'on vient d'insérée
    question_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return {"question_id": question_id}, 200

if __name__ == "__main__":	
    app.run()
    