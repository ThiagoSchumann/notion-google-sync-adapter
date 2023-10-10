from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import os.path


class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, token_path, credentials_path):
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.creds = self._setup_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _setup_credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=8081)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_upcoming_events(self, calendar_id='primary', max_results=10):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId=calendar_id, timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
