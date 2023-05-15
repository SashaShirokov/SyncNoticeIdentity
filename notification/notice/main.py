from notify_service import notify_team
from email_service import get_outlook_system, get_gmail_system


def main():
    outlook_system = get_outlook_system()
    notify_team(outlook_system)

    # gmail_system = get_gmail_system()
    # notify_team(gmail_system)


if __name__ == "__main__":
    main()
