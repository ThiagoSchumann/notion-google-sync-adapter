import unittest
from unittest.mock import patch, Mock
# Ajuste o import conforme necessário
from src.core.google_calendar_service import GoogleCalendarService


class TestGoogleCalendarService(unittest.TestCase):
    @patch('src.core.google_calendar_service.build')
    def setUp(self, mock_build):
        # Definindo mock para o serviço Google Calendar
        self.mock_service = Mock()
        mock_build.return_value = self.mock_service

        # Instanciando o objeto a ser testado
        self.calendar_service = GoogleCalendarService(
            '.\\.credentials\\token.json',
            '.\\.credentials\\credentials.json'
        )

    def test_get_upcoming_events_success(self):
        # Definindo resposta mock para o método list().execute() do serviço
        self.mock_service.events().list().execute.return_value = {
            'items': [{'summary': 'Event 1'}, {'summary': 'Event 2'}]
        }

        # Chamando o método a ser testado
        result = self.calendar_service.get_upcoming_events()

        # Verificando se o resultado é o esperado
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['summary'], 'Event 1')
        self.assertEqual(result[1]['summary'], 'Event 2')

    def test_get_upcoming_events_no_events(self):
        # Definindo resposta mock sem eventos
        self.mock_service.events().list().execute.return_value = {}

        # Chamando o método a ser testado
        result = self.calendar_service.get_upcoming_events()

        # Verificando se o resultado é uma lista vazia
        self.assertEqual(result, [])

    def test_get_upcoming_events_error(self):
        # Definindo o método list().execute() do serviço para lançar uma exceção
        self.mock_service.events().list().execute.side_effect = Exception('Error')

        # Chamando o método a ser testado e verificando se ele retorna uma lista vazia
        with self.assertRaises(Exception):
            self.calendar_service.get_upcoming_events()


if __name__ == '__main__':
    unittest.main()
