import unittest

from src.sqlite.cache_db import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.db = CacheDB()

    def test_connection(self):  # i nomi dei metodi di test devono iniziare con "test"
        self.assertIsNotNone(self.db.conn)  # controllo che la connessione non sia None

    def test_topic(self):
        # CREATE: controllo se un topic è stato inserito correttamente
        self.db.save_all_topics([Topic(999, "Topic999", "Un topic 999")])  # READ
        topic = self.db.get_topic(999)
        self.assertIsNotNone(topic)
        # TODO: UPDATE topic
        # DELETE: controllo se un topic è stato eliminato correttamente
        self.db.delete_topic(999)
        topic_none = self.db.get_topic(999)
        self.assertIsNone(topic_none)


if __name__ == '__main__':
    unittest.main()
