import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, body):
    msg = MIMEText(body, 'html')
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_SENDER")
    msg["To"] = to_email

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email send error:", e)
        return False
