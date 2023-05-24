import json
import sqlite3

from flask import request

################################################################################
#                                 CLASSE                                       #
################################################################################

class Question:
    def __init__(self, position: int, title: str, text: str, image: str, possibleAnswers: list):
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possibleAnswers = possibleAnswers

    # Sérialisation Objet Question -> Données JSON
    def serialize(self):
        question_dict = {
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": self.possibleAnswers
        }

        return json.dumps(question_dict)

    # Désérialisation Données JSON -> Objet Question
    def deserialize(json_data):
        question_dict = json.loads(json_data)

        position = question_dict.get("position")
        title = question_dict.get("title")
        text = question_dict.get("text")
        image = question_dict.get("image")
        possibleAnswers = question_dict.get("possibleAnswers")

        return Question(position, title, text, image, possibleAnswers)
    
    # Getter - Retourne les réponses via l'ID de la question 
    def get_answers_by_question_id(question_id):
        conn = sqlite3.connect('./quiz-questions.db')
        cursor = conn.cursor()

        query = "SELECT text, is_correct FROM quiz_answers WHERE question_id = ?"
        cursor.execute(query, (question_id,))
        results = cursor.fetchall()

        conn.close()

        answers = [{"text": row[0], "isCorrect": bool(row[1])} for row in results]
        return answers

    # Getter - Retourne la question via l'ID
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

    # Getter - Retourne la question via la position
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

# Génération de la requête SQL et des paramètres pour insérer une question dans la table quiz_questions
def generate_insert_questions_query(question):
    query = "INSERT INTO quiz_questions (position, title, text, image) VALUES (?, ?, ?, ?)"
    params = (question.position, question.title, question.text, question.image)

    return query, params

# Génération de la requête SQL et des paramètres pour insérer les réponses possibles d'une question dans la table quiz_answers
def generate_insert_answers_query(question_id, possibleAnswers):
    query = "INSERT INTO quiz_answers (question_id, text, is_correct) VALUES (?, ?, ?)"
    params = [(question_id, answer["text"], answer["isCorrect"]) for answer in possibleAnswers]

    return query, params

# Génération d'un objet Question à partir des données de la base de données
def generate_question_object(result):
    question_id, position, title, text, image = result

    possibleAnswers = Question.get_answers_by_question_id(question_id)

    return Question(position, title, text, image, possibleAnswers)

################################################################################
#                                  GETTER                                      #
################################################################################

# Getter - Retourne le nombre de question dans la base de données
def get_question_count():
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM quiz_questions")
    size = cursor.fetchone()[0]

    conn.close()

    return size

# Getter - Retourne les scores dans la base de données
def get_scores():
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    select_query = "SELECT player_name, score FROM quiz_participations ORDER BY score DESC"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    scores = []
    for row in rows:
        player_name = row[0]
        score = row[1]

        score_entry = {
            "playerName": player_name,
            "score": score
        }
        scores.append(score_entry)

    conn.close()

    return scores

################################################################################
#                                INSERTION                                     #
################################################################################

# Insertion d'une question dans la base de données (prise en compte de la position)
def add_question():
    # Récupération des données de la question envoyées dans le corps de la requête JSON
    question_data = request.get_json()

    # Création d'une instance de la classe Question avec les données de la question
    question = Question(question_data['position'], question_data['title'], question_data['text'], question_data['image'],
                        question_data['possibleAnswers'])

    # Vérification de l'existence d'une question à la même position
    existing_question = Question.get_question_by_position(question.position)
    
    if existing_question:
        # Décalage des positions des questions existantes après la position actuelle
        conn = sqlite3.connect('./quiz-questions.db')
        cursor = conn.cursor()
        shift_position_query = "UPDATE quiz_questions SET position = position + 1 WHERE position >= ?"
        cursor.execute(shift_position_query, (question.position,))
        conn.commit()
        conn.close()

    # Génération de la requête SQL insert pour la question
    insert_query, params = generate_insert_questions_query(question)

    # Insertion de la question dans la base de données
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()
    cursor.execute(insert_query, params)
    
    # Récupération de l'identifiant de la question que l'on vient d'insérer
    question_id = cursor.lastrowid

    # Génération de la requête SQL insert pour les réponses possibles
    insert_answers_query, answers_params = generate_insert_answers_query(question_id, question.possibleAnswers)

    # Insertion des réponses possibles dans la base de données
    cursor.executemany(insert_answers_query, answers_params)

    conn.commit()
    conn.close()

    return {"id": question_id}, 200

################################################################################
#                               SUPPRESSION                                    #
################################################################################

# Suppression de toutes les questions de la base de données
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

# Suppression d'une question de la base de donnée selon son ID
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
        shift_position_query = "UPDATE quiz_questions SET position = position - 1 WHERE position > ?"
        cursor.execute(shift_position_query, (question.position,))

        conn.commit()
        conn.close()

        return "Question deleted", 204
    else:
        return "Question not found", 404

# Suppression de toutes les participations de la base de données
def del_all_participations():
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    delete_participations_query = "DELETE FROM quiz_participations"
    delete_sequence_query = "DELETE FROM sqlite_sequence WHERE name = 'quiz_participations'"

    cursor.execute(delete_participations_query)
    cursor.execute(delete_sequence_query)

    conn.commit()
    conn.close()

    return "Deleted all participations", 204

################################################################################
#                                 LECTURE                                      #
################################################################################

# Lecture d'une question via son ID
def read_question_by_id(question_id):
    question = Question.get_question_by_id(question_id)

    if question:
        return question.serialize(), 200
    else:
        return "Question not found", 404
    
# Lecture d'une question via sa position
def read_question_by_position(position):
    question = Question.get_question_by_position(position)

    if question:
        return question.serialize(), 200
    else:
        return "Question not found", 404
    
################################################################################
#                                  UPDATE                                      #
################################################################################

# Mise à jour d'une question
def update_question(question_id):
    # Récupération des données de la question envoyées dans le corps de la requête JSON
    question_data = request.get_json()

    # Vérification de l'existence de la question
    question = Question.get_question_by_id(question_id)
    if not question:
        return "Question not found", 404

    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    # Mise à jour des attributs de la question avec les nouvelles données
    question.text = question_data.get('text', question.text)
    question.title = question_data.get('title', question.title)
    question.image = question_data.get('image', question.image)

    update_question_query = "UPDATE quiz_questions SET text = ?, title = ?, image = ? WHERE question_id = ?"
    update_params = (question.text, question.title, question.image, question_id)
    cursor.execute(update_question_query, update_params)

    # Suppression des réponses existantes de la question
    delete_query = "DELETE FROM quiz_answers WHERE question_id = ?"
    cursor.execute(delete_query, (question_id,))

    # Mise à jour des nouvelles réponses de la question
    new_possible_answers = question_data.get('possibleAnswers', question.possibleAnswers)
    for answer_data in new_possible_answers:
        text = answer_data.get('text', '')
        is_correct = answer_data.get('isCorrect', False)

        update_answer_query = "INSERT INTO quiz_answers (question_id, text, is_correct) VALUES (?, ?, ?)"
        cursor.execute(update_answer_query, (question_id, text, is_correct))

    # Récupération de la position de destination à partir des données JSON
    destination_position = question_data.get('position')
    if destination_position is not None:
        # Vérification si une question existe déjà à la position de destination
        existing_question = Question.get_question_by_position(destination_position)

        # Si une question existe déjà à la position de destination,
        # il faut décaler toutes les questions entre la position actuelle et la position de destination
        if existing_question and destination_position != question.position:
            if destination_position > question.position:
                # Décalage des questions vers le bas (positions supérieures)
                shift_down_query = "UPDATE quiz_questions SET position = position - 1 WHERE position > ? AND position <= ?"
                cursor.execute(shift_down_query, (question.position, destination_position))
            else:
                # Décalage des questions vers le haut (positions inférieures)
                shift_up_query = "UPDATE quiz_questions SET position = position + 1 WHERE position < ? AND position >= ?"
                cursor.execute(shift_up_query, (question.position, destination_position))

            # Décalage de la question actuelle vers la position de destination
            update_position_query = "UPDATE quiz_questions SET position = ? WHERE question_id = ?"
            cursor.execute(update_position_query, (destination_position, question_id))

    conn.commit()
    conn.close()

    return "Question updated", 204

################################################################################
#                               PARTICIPATION                                  #
################################################################################

# Insertion d'une participation dans la base de données
def add_participation():
    participation_data = request.get_json()
    player_name = participation_data['playerName']
    answers = participation_data['answers']
    score = 0

    if len(answers) < 10:
        return "Bad request - Incomplete participation", 400

    if len(answers) > 10:
        return "Bad request - Overcomplete participation", 400

    # Calcul du score en vérifiant les réponses de l'utilisateur
    for i, answer in enumerate(answers):
        question = Question.get_question_by_position(i + 1)
        if question is not None:
            selected_answer = question.possibleAnswers[answer - 1]
            if selected_answer['isCorrect']:
                score += 1

    # Insertion de la participation dans la table "quiz_participations"
    conn = sqlite3.connect('./quiz-questions.db')
    cursor = conn.cursor()

    insert_query = "INSERT INTO quiz_participations (player_name, answers, score) VALUES (?, ?, ?)"
    cursor.execute(insert_query, (player_name, json.dumps(answers), score))

    conn.commit()
    conn.close()

    return {"playerName": player_name, "score": score}, 200
