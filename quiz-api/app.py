from flask import Flask, request
from flask_cors import CORS

import hashlib

from auth_utils import authenticate
from jwt_utils import build_token
from db_utils import generate_database
from question_utils import add_participation, add_question, del_all_participations, del_all_questions, del_question_by_id, get_question_count, get_scores, read_question_by_id, read_question_by_position, update_question

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
    size = get_question_count()
    scores = get_scores()

    return {"size": size, "scores": scores}, 200

################################################################################
#                             AUTHENTIFICATION                                 #
################################################################################

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

################################################################################
#                                INSERTION                                     #
################################################################################

# Endpoint pour ajouter une question
@app.route('/questions', methods=['POST'])
def PostAddQuestion():
    # Vérification de l'authentification
    auth = authenticate()
    
    if isinstance(auth, tuple):
        return auth
    
    return add_question()

################################################################################
#                               SUPPRESSION                                    #
################################################################################

# Endpoint pour supprimer toutes les questions
@app.route('/questions/all', methods=['DELETE'])
def DeleteAllQuestions():
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	
	return del_all_questions()

# Endpoint pour supprimer une question selon son ID
@app.route('/questions/<question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):  
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	  
	return del_question_by_id(question_id)

# Endpoint pour supprimer toutes les participations
@app.route('/participations/all', methods=['DELETE'])
def DeleteAllParticipations():
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	
	return del_all_participations()

################################################################################
#                                 LECTURE                                      #
################################################################################

# Endpoint pour lire une question selon son ID
@app.route('/questions/<question_id>', methods=['GET'])
def GetQuestionByID(question_id):  
	return read_question_by_id(question_id)

# ENdpoint pour lire une question selon sa position
@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
    position = int(request.args.get('position'))
    return read_question_by_position(position)

################################################################################
#                                  UPDATE                                      #
################################################################################

# Endpoint pour mettre à jour une question
@app.route('/questions/<question_id>', methods=['PUT'])
def PutQuestion(question_id):
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	
	return update_question(question_id)

################################################################################
#                               PARTICIPATION                                  #
################################################################################

# Endpoint pour ajouter une participation
@app.route('/participations', methods=['POST'])
def PostParticipation():
    return add_participation()

################################################################################
#                                   RUN                                        #
################################################################################

# Endpoint pour recréer la base de données
@app.route('/rebuild-db', methods=['POST'])
def PostRebuildDB():
    # Vérification de l'authentification
	auth = authenticate()

	if isinstance(auth, tuple):
		return auth
	
	return generate_database()

if __name__ == "__main__":	
    app.run()
    