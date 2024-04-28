import mysql.connector
import csv

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="kareem2478",
    )

def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydb;")
    cursor.execute("USE mydb;")

def create_tables(cursor):
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """

    scores_table = """
    CREATE TABLE IF NOT EXISTS scores (
        score_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        score INT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """

    quizzes_table = """
    CREATE TABLE IF NOT EXISTS quizzes (
        quiz_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        is_custom TINYINT(1) NOT NULL DEFAULT 0,
        is_public TINYINT(1),
        user_id INT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """

    questions_table = """
    CREATE TABLE IF NOT EXISTS questions (
        question_id INT PRIMARY KEY,
        quiz_id INT,
        question_text TEXT NOT NULL,
        option_1 VARCHAR(255) NOT NULL,
        option_2 VARCHAR(255) NOT NULL,
        option_3 VARCHAR(255) NOT NULL,
        option_4 VARCHAR(255) NOT NULL,
        correct_option INT NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
    );
    """

    cursor.execute(users_table)
    cursor.execute(scores_table)
    cursor.execute(quizzes_table)
    cursor.execute(questions_table)
    
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        return list(reader)

def check_and_insert_data(cursor, quizzes_path, questions_path):
    # Check existing quiz_ids 1 to 4
    cursor.execute("SELECT quiz_id FROM quizzes WHERE quiz_id BETWEEN 1 AND 4")
    existing_ids = {quiz_id[0] for quiz_id in cursor.fetchall()}

    # Read quiz data and insert if not exists
    quizzes_data = read_csv(quizzes_path)
    for row in quizzes_data:
        quiz_id = int(row[0])
        if quiz_id not in existing_ids:
            # Check user_id field; default to 0 if empty or non-digit
            user_id = int(row[4]) if row[4].isdigit() else 0
            cursor.execute("""
            INSERT INTO quizzes (quiz_id, title, is_custom, is_public)
            VALUES (%s, %s, %s, %s)
            """, (quiz_id, row[1], row[2], row[3]))

    # Read question data
    questions_data = read_csv(questions_path)

    # Find which question IDs in the range 1 to 20 are missing from the database
    cursor.execute("SELECT question_id FROM questions WHERE question_id BETWEEN 1 AND 20")
    existing_question_ids = {row[0] for row in cursor.fetchall()}
    missing_ids = set(range(1, 21)).difference(existing_question_ids)

    # Insert missing question data
    for row in questions_data:
        question_id = int(row[0])
        if question_id in missing_ids:
            cursor.execute("""
            INSERT INTO questions (question_id, quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))

def setup_database():
    db = create_db_connection()
    cursor = db.cursor()
    create_database(cursor)
    create_tables(cursor)
    check_and_insert_data(cursor, 'quizzes.csv', 'questions.csv')
    db.commit()
    return db,cursor

setup_database()
