import hashlib
import mysql.connector
import re

from db import get_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Username validation
def is_valid_username(username):
    return username.replace(" ", "").isalpha()


# Email validation
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def register(username, email, password):

    # Empty fields check
    if not username or not email or not password:
        return "empty_fields"

    # Username check
    if not is_valid_username(username):
        return "wrong_username"

    # Email check
    if not is_valid_email(email):
        return "invalid_email"

    # Password length check
    if len(password) < 6:
        return "weak_password"

    conn = get_db()
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:

        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s,%s,%s)",
            (username, email, hashed)
        )

        conn.commit()
        return "success"

    except mysql.connector.IntegrityError:
        conn.rollback()
        return "email_exists"

    except Exception as e:
        conn.rollback()
        return f"error: {e}"

    finally:
        conn.close()


def login(username, password):

    conn = get_db()
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute(
        "SELECT id, username, email FROM users WHERE username=%s AND password_hash=%s",
        (username, hashed)
    )

    user = cursor.fetchone()

    conn.close()

    return user