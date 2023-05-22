import json
import sqlite3

from flask import request

################################################################################
#                                 CLASSE                                       #
################################################################################

class Question:
    def __init__(self, position: int, title: str, text: str, image: str, answers: list):
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.answers = answers

    def serialize(self):
        question_dict = {
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "answers": self.answers
        }

        return json.dumps(question_dict)

    def deserialize(json_data):
        question_dict = json.loads(json_data)

        position = question_dict.get("position")
        title = question_dict.get("title")
        text = question_dict.get("text")
        image = question_dict.get("image")
        answers = question_dict.get("answers")

        return Question(position, title, text, image, answers)
    
    def get_question_by_id(question_id):
        conn = sqlite3.connect('./quiz-questions.db')
        cursor = conn.cursor()

        query = "SELECT * FROM quiz_questions WHERE question_id = ?"
        cursor.execute(query, (question_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return generate_question_object(result)
        else:
            return None

    def get_question_by_position(position):
        conn = sqlite3.connect('./quiz-questions.db')
        cursor = conn.cursor()

        query = "SELECT * FROM quiz_questions WHERE position = ?"
        cursor.execute(query, (position,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return generate_question_object(result)
        else:
            return None
        
################################################################################
#                                GENERATION                                    #
################################################################################

def generate_insert_questions_query(question):
    query = "INSERT INTO quiz_questions (position, title, text, image) VALUES (?, ?, ?, ?)"
    params = (question.position, question.title, question.text, question.image)

    return query, params

def generate_insert_answers_query(question_id, answers):
    query = "INSERT INTO quiz_answers (question_id, text, is_correct) VALUES (?, ?, ?)"
    params = [(question_id, answer["text"], answer["isCorrect"]) for answer in answers]

    return query, params

def generate_question_object(result):
    question_id, position, title, text, image = result

    return Question(question_id, position, title, text, image)

################################################################################
#                                INSERTION                                     #
################################################################################

def add_question():
    # Récupération des données de la question envoyées dans le corps de la requête JSON
    question_data = request.get_json()

    # Création d'une instance de la classe Question avec les données de la question
    question = Question(question_data['position'], question_data['title'], question_data['text'], question_data['image'],
                        question_data['possibleAnswers'])

    # Génération de la requête SQL insert pour la question
    insert_query, params = generate_insert_questions_query(question)

    # Insertion de la question dans la base de données
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()
    cursor.execute(insert_query, params)
    
    # Récupération de l'identifiant de la question que l'on vient d'insérer
    question_id = cursor.lastrowid

    # Génération de la requête SQL insert pour les réponses possibles
    insert_answers_query, answers_params = generate_insert_answers_query(question_id, question.answers)

    # Insertion des réponses possibles dans la base de données
    cursor.executemany(insert_answers_query, answers_params)

    conn.commit()
    conn.close()

    return {"question_id": question_id}, 200

################################################################################
#                               SUPPRESSION                                    #
################################################################################

def del_all_questions():
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    delete_questions_query = "DELETE FROM quiz_questions"
    delete_answers_query = "DELETE FROM quiz_answers"
    delete_sequence_query = "DELETE FROM sqlite_sequence"

    cursor.execute(delete_answers_query)
    cursor.execute(delete_questions_query)
    cursor.execute(delete_sequence_query)

    conn.commit()
    conn.close()

    return "Deleted all questions", 204

def del_question_by_id(question_id):
    question = Question.get_question_by_id(question_id)

    if question:
        conn = sqlite3.connect('./quiz-questions.db')
        cursor = conn.cursor()

        delete_question_query = "DELETE FROM quiz_questions WHERE question_id = ?"
        cursor.execute(delete_question_query, (question_id,))

        delete_answers_query = "DELETE FROM quiz_answers WHERE question_id = ?"
        cursor.execute(delete_answers_query, (question_id,))

        # Décalage de la position des questions après la suppression
        cursor.execute(
        "UPDATE quiz_questions SET position = position + ? WHERE position >= ?",
        (-1, question.position),
        )

        conn.commit()
        conn.close()

        return "Question deleted", 204
    else:
        return "Question not found", 404