import unittest

from src.sqlite.cache_db import *


class MyTestCase(unittest.TestCase):
    def test_connection(self):  # i nomi dei metodi di test devono iniziare con "test"
        db = CacheDB()
        self.assertIsNotNone(db.conn)  # controllo che la connessione non sia None


if __name__ == '__main__':
    unittest.main()
