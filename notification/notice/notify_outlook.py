from pathlib import Path
import smtplib
from email.message import EmailMessage

from config import (
    OUTLOOK_EMAIL_ADDRESS,
    OUTLOOK_EMAIL_PASSWORD,
    OUTLOOK_SERVER,
    OUTLOOK_PORT,
    PASS,
    ALERT,
    PATH_TO_APP_LOCAL,
    PATH_TO_APP_DOCKER,
)


CONTACTS = [OUTLOOK_EMAIL_ADDRESS]


def notify_team_outlook():
    with smtplib.SMTP(OUTLOOK_SERVER, OUTLOOK_PORT) as smtp:
        message = _build_message()
        smtp.send_message(message)


def _build_message() -> EmailMessage:
    message = EmailMessage()
    message["From"] = OUTLOOK_EMAIL_ADDRESS
    message["To"] = CONTACTS
    message["Subject"] = "Scan Notice"
    vulnerable = _is_vulnerable()
    if vulnerable:
        message_html = _get_message_html(color=ALERT["color"], message=ALERT["message"])
    else:
        message_html = _get_message_html(color=PASS["color"], message=PASS["message"])
    message.add_alternative(message_html, subtype="html")

    # attaching the output of osv-scanner
    file_data, file_name = _get_attachment()
    message.add_attachment(file_data, filename=file_name)
    return message


def _is_vulnerable() -> bool:
    with open(Path(PATH_TO_APP_DOCKER) / "scan.txt") as file:
        lines = len(file.readlines())
    # with open(Path(PATH_TO_APP_LOCAL) / "scan.txt") as file:
    #     lines = len(file.readlines())
    return True if lines > 1 else False


def _get_message_html(color: str, message: str) -> str:
    message_html = f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color:{color};">{message}</h1>
            </body>
        </html>
        """
    return message_html


def _get_attachment() -> tuple:
    with open(Path(PATH_TO_APP_DOCKER) / "scan.txt") as file:
        file_data = file.read()
        file_name = file.name
    # with open(Path(PATH_TO_APP_LOCAL) / "scan.txt") as file:
    #     file_data = file.read()
    #     file_name = file.name
    return file_data, file_name


if __name__ == "__main__":
    notify_team()
