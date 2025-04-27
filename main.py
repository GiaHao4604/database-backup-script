# main.py

import schedule
import time
from backup import backup_database

def run_scheduler():
    schedule.every().day.at("00:00").do(backup_database)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Kiểm tra mỗi phút

if __name__ == "__main__":
    run_scheduler()
