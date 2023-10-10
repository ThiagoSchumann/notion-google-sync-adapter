import unittest
from unittest.mock import patch, Mock
from src.core.google_calendar_service import GoogleCalendarService


class TestGoogleCalendarService(unittest.TestCase):

    @patch('src.core.google_calendar_service.build')
    @patch('src.core.google_calendar_service.InstalledAppFlow')
    @patch('src.core.google_calendar_service.Credentials')
    @patch('src.core.google_calendar_service.os.path.exists', return_value=True)
    def setUp(self, mock_exists, mock_credentials, mock_flow, mock_build):
        self.token_path = '.\\.credentials\\token.json'
        self.credentials_path = '.\\.credentials\\credentials.json'
        self.gcal_service = GoogleCalendarService(
            self.token_path, self.credentials_path)

    def test_setup_credentials_with_existing_token(self):
        self.gcal_service._setup_credentials()
        self.gcal_service.creds.from_authorized_user_file.assert_called_once_with(
            self.token_path, self.gcal_service.SCOPES)

    @patch('src.core.google_calendar_service.os.path.exists', return_value=False)
    def test_setup_credentials_with_no_token(self, mock_exists):
        self.gcal_service._setup_credentials()
        self.gcal_service.flow.run_local_server.assert_called_once()

    @patch('src.core.google_calendar_service.os.path.exists', return_value=True)
    def test_setup_credentials_with_expired_token(self, mock_exists):
        self.gcal_service.creds.expired = True
        self.gcal_service.creds.refresh_token = True
        self.gcal_service._setup_credentials()
        self.gcal_service.creds.refresh.assert_called_once()

    @patch('src.core.google_calendar_service.HttpError', side_effect=Exception)
    def test_get_upcoming_events_with_error(self, mock_error):
        events = self.gcal_service.get_upcoming_events()
        self.assertEqual(events, [])
        self.assertTrue(mock_error.called)

    @patch('src.core.google_calendar_service.build')
    def test_get_upcoming_events_with_success(self, mock_build):
        mock_build.return_value.events.return_value.list.return_value.execute.return_value = {
            'items': ['event1', 'event2']}
        events = self.gcal_service.get_upcoming_events()
        self.assertEqual(events, ['event1', 'event2'])


if __name__ == '__main__':
    unittest.main()
