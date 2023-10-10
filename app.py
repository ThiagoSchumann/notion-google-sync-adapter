from src.core.google_calendar_service import GoogleCalendarService


def main():
    gcal_service = GoogleCalendarService(
        '.\\.credentials\\token.json',
        '.\\.credentials\\credentials.json'
    )
    events = gcal_service.get_upcoming_events()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == "__main__":
    main()
