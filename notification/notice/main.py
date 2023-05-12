from notify_outlook import notify_team_outlook
from notify_service import notify_team
from email_service import get_gmail_system, get_outlook_system


def main():
    gmail_system = get_gmail_system()
    notify_team(gmail_system)

    # outlook_system = get_outlook_system()
    # notify_team(outlook_system)
    print("hey")


if __name__ == "__main__":
    main()
