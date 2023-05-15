import os
import datetime
import smtplib
from pathlib import Path
from email.message import EmailMessage

from config import OUTLOOK_CONTACTS, PATH_TO_APP_DOCKER, PASS, ALERT


def notify_team(email_system):
    if email_system.name == "GMAIL":
        with smtplib.SMTP_SSL(email_system.server, email_system.port) as smtp:
            smtp.login(email_system.address, email_system.password)
            message = _build_message(email_system.address)
            smtp.send_message(message)

    if email_system.name == "OUTLOOK":
        with smtplib.SMTP(email_system.server, email_system.port) as smtp:
            message = _build_message(email_system.address)
            smtp.send_message(message)


def _build_message(sender_address) -> EmailMessage:
    file_data, file_name, file_datetime = _get_attachment()
    message = EmailMessage()
    message["From"] = sender_address
    message["To"] = OUTLOOK_CONTACTS
    message["Subject"] = f"Scanned {file_datetime}"

    vulnerable = _is_vulnerable()
    if vulnerable:
        message_html = _get_message_html(color=ALERT["color"], message=ALERT["message"])
    else:
        message_html = _get_message_html(color=PASS["color"], message=PASS["message"])
    message.add_alternative(message_html, subtype="html")

    # attaching the output of osv-scanner
    message.add_attachment(file_data, filename=file_name)
    return message


def _is_vulnerable() -> bool:
    with open(Path(PATH_TO_APP_DOCKER) / "scan.txt") as file:
        lines = len(file.readlines())
    return True if lines > 1 else False


def _get_message_html(color: str, message: str) -> str:
    message_html = f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Hello!</h1>
                <h2 style="color:{color};">{message}</h2>
                <p> Scan was fulfilled by osv-scanner.</p>
            </body>
        </html>
        """
    return message_html


def _get_attachment() -> tuple:
    with open(Path(PATH_TO_APP_DOCKER) / "scan.txt") as file:
        file_data = file.read()
        file_name = file.name
        unix_time = os.path.getmtime(Path(PATH_TO_APP_DOCKER) / "scan.txt")
        file_datetime = datetime.datetime.utcfromtimestamp(unix_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    return file_data, file_name, file_datetime
