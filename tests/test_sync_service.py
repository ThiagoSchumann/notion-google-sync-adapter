import unittest
from src.core.sync_service import SyncService


class TestSyncService(unittest.TestCase):
    def test_sync(self):
        service = SyncService()
        result = service.sync()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
