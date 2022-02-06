import unittest

from src.sqlite.cache_db import *


class MyTestCase(unittest.TestCase):
    def test_connection(self):  # i nomi dei metodi di test devono iniziare con "test"
        db = CacheDB()
        self.assertIsNotNone(db.conn)  # controllo che la connessione non sia None

    def test_topic(self):
        db = CacheDB()
        # CREATE: controllo se un topic è stato inserito correttamente
        db.save_all_topics([Topic(999, "Topic999", "Un topic 999")])  # READ
        topic = db.get_topic(999)
        self.assertIsNotNone(topic)
        # TODO: UPDATE topic
        # DELETE: controllo se un topic è stato eliminato correttamente
        db.remove_topic(999)
        topic_none = db.get_topic(999)
        self.assertIsNone(topic_none)


if __name__ == '__main__':
    unittest.main()
