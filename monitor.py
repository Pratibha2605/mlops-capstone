import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import random

LOG_FILE = "logs.txt"
ERROR_THRESHOLD = 0.3  # 30% of logs are errors
CHECK_INTERVAL = 10    # seconds

# Email configuration (replace with GitHub secrets if using GitHub Actions)
GMAIL_USER = "pratibhamahadik08@gmail.com"
GMAIL_PASSWORD = "ozst tjyo ldck lerq"
TO_EMAIL = "pratibha.mahadik@sdbi.in"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_email_alert(error_rate):
    subject = "ALERT! Error rate exceeded threshold"
    body = f"Current error rate is {error_rate:.2f}, threshold is {ERROR_THRESHOLD:.2f}"

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Alert sent via email: {body}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def generate_mock_log():
    if random.random() < 0.7:
        logging.info(f"Prediction successful: input={random.randint(1,100)}, output={random.uniform(1,100):.2f}")
    else:
        logging.error(f"Prediction failed: input={random.randint(-50,0)}, error=Mock bad data")

print("Monitor started...")
while True:
    generate_mock_log()  # simulate logs
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    if not lines:
        time.sleep(CHECK_INTERVAL)
        continue
    total_logs = len(lines)
    error_logs = sum(1 for line in lines if "ERROR" in line)
    error_rate = error_logs / total_logs
    print(f"Total logs: {total_logs}, Errors: {error_logs}, Error rate: {error_rate:.2f}")
    if error_rate > ERROR_THRESHOLD:
        send_email_alert(error_rate)
    time.sleep(CHECK_INTERVAL)
