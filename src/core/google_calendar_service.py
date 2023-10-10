from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class GoogleCalendarService:
    def __init__(self, credentials_path):
        self.credentials = Credentials.from_authorized_user_file(
            credentials_path)
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_upcoming_events(self, calendar_id='primary', max_results=10):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId=calendar_id, timeMin=now, maxResults=max_results,
            singleEvents=True, orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
