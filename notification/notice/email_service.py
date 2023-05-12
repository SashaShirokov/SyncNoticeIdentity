from config import (
    GMAIL_SERVER,
    GMAIL_PORT,
    GMAIL_EMAIL_ADDRESS,
    GMAIL_EMAIL_PASSWORD,
    OUTLOOK_SERVER,
    OUTLOOK_PORT,
    OUTLOOK_EMAIL_ADDRESS,
)


class EmailSystem:
    def __init__(
        self,
        email_name,
        email_server,
        email_port,
        email_address,
        email_password=None,
    ):
        self.email_name = email_name
        self.email_server = email_server
        self.email_port = email_port
        self.email_address = email_address
        self.email_password = email_password

    @property
    def name(self):
        return self.email_name

    @property
    def server(self):
        return self.email_server

    @property
    def port(self):
        return self.email_port

    @property
    def address(self):
        return self.email_address

    @property
    def password(self):
        return self.email_password


def get_gmail_system() -> EmailSystem:
    gmail_system = EmailSystem(
        email_name="GMAIL",
        email_server=GMAIL_SERVER,
        email_port=GMAIL_PORT,
        email_address=GMAIL_EMAIL_ADDRESS,
        email_password=GMAIL_EMAIL_PASSWORD,
    )
    return gmail_system


def get_outlook_system() -> EmailSystem:
    # in Godel's outlook no need for login
    outlook_system = EmailSystem(
        email_name="OUTLOOK",
        email_server=OUTLOOK_SERVER,
        email_port=OUTLOOK_PORT,
        email_address=OUTLOOK_EMAIL_ADDRESS,
    )
    return outlook_system
