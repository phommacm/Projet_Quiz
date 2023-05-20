import sqlite3
from flask import request
from jwt_utils import decode_token
from jwt_utils import JwtError

def add_question():
    # Récupération des données de la question envoyées dans le corps de la requête JSON
    question_data = request.get_json()
    
    # Vérification de l'authentification
    auth_header = request.headers.get('Authorization')
    
    if auth_header is not None:
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
    
    # Récupération de l'identifiant de la question que l'on vient d'insérer
    question_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return {"question_id": question_id}, 200