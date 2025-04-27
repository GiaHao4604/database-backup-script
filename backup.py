# backup.py

import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load .env file
load_dotenv()

# Cấu hình thông tin mail
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
DB_DIR = os.getenv("DB_DIR", "./databases")
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")

# Tạo thư mục backup nếu chưa tồn tại
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def backup_database():
    try:
        for filename in os.listdir(DB_DIR):
            if filename.endswith(".sql") or filename.endswith(".sqlite3"):
                file_path = os.path.join(DB_DIR, filename)
                backup_file = os.path.join(BACKUP_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}")
                shutil.copy(file_path, backup_file)
                print(f"Backup successful: {backup_file}")
        
        send_email("Backup successful", "The database backup has been completed successfully.")
    except Exception as e:
        send_email("Backup failed", f"The database backup failed. Error: {str(e)}")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
            print(f"Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
