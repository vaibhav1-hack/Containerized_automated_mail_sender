import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime

# ====== CONFIG (EDIT THESE) ======
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "boathack0@gmail.com"
SMTP_PASS = "bofwoekyrirjocli"
TO_EMAIL  = "vaibhavswarnkar281@gmail.com"

LOG_FILE = Path("/var/log/server_update.log")
# ================================

def main():
    if not LOG_FILE.exists():
        return

    content = LOG_FILE.read_text(errors="ignore").strip()
    if not content:
        return

    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"Server Update Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.set_content(content)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    main()
