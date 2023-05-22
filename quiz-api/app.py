from flask import Flask, request
from flask_cors import CORS

import hashlib

from auth_utils import authenticate
from jwt_utils import build_token
from question_utils import add_question, del_all_questions, del_question_by_id

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
    # Vérification de l'authentification
    auth = authenticate()
    
    if isinstance(auth, tuple):
        return auth
    
    return add_question()


# Endpoint pour supprimer toutes les questions
@app.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	
	return del_all_questions()

@app.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):  
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	  
	return del_question_by_id(question_id)

if __name__ == "__main__":	
    app.run()
    