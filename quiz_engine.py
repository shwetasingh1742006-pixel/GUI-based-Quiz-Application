from db import get_db

def get_categories():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM categories")
    data = cursor.fetchall()

    conn.close()
    return data

def get_questions(category_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question_text, option_a, option_b, option_c, option_d, correct_answer
        FROM questions WHERE category_id=%s
    """, (category_id,))

    data = cursor.fetchall()
    conn.close()
    return data

def save_result(user_id, score, total, category_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_results (user_id, score, total_questions, category_id)
        VALUES (%s,%s,%s,%s)
    """, (user_id, score, total, category_id))

    conn.commit()
    conn.close()