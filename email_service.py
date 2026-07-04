import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

EMAIL = "yourrealgmail@gmail.com"
PASSWORD = "juadbhbzilpppiiy"

def send_result(to_email, score, total):

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Quiz Result"

        body = f"""
Hello User,

Your quiz has been completed successfully.

Your Score: {score}/{total}

Thank you for using Quiz System.
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 465)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        messagebox.showinfo("success","Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Wrong Email or Wrong App Password")

    except Exception as e:
        print("Send Successfully ")