import os
import sqlite3

# Chemin vers la base de données SQLite
db_path = "quiz-questions.db"

# Fonction pour générer la base de données avec les tables
def generate_database():
    # Suppression de la base de données si elle existe déjà
    if os.path.exists(db_path):
        os.remove(db_path)

    # Création d'un nouveau fichier de base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Création de la table quiz_questions
    cursor.execute('''CREATE TABLE quiz_questions (
                        question_id INTEGER NOT NULL,
                        position INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        text TEXT NOT NULL,
                        image TEXT NOT NULL,
                        PRIMARY KEY(question_id AUTOINCREMENT)
                    )''')

    # Création de la table quiz_answers
    cursor.execute('''CREATE TABLE quiz_answers (
                        answer_id INTEGER NOT NULL,
                        question_id INTEGER NOT NULL,
                        text TEXT NOT NULL,
                        is_correct INTEGER NOT NULL,
                        PRIMARY KEY(answer_id AUTOINCREMENT)
                    )''')

    # Création de la table quiz_participations
    cursor.execute('''CREATE TABLE quiz_participations (
                        participation_id INTEGER NOT NULL,
                        player_name TEXT NOT NULL,
                        answers TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        PRIMARY KEY(participation_id AUTOINCREMENT)
                    )''')

    conn.close()

    return "Ok", 200