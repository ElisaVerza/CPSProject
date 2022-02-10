import unittest
from typing import List

from src.api import fetch
from src.sqlite import cache_db
from src.wb.Indicator import Indicator


class ApiTestCase(unittest.TestCase):
    def test_all_topics(self):
        # prima elimino tutti i topic dal database
        db = cache_db.CacheDB()
        db.delete_all_topics()

        # li scarico
        downloaded_topics = fetch.all_topics()

        # controllo che siano stati scaricati dati
        self.assertTrue(len(downloaded_topics) > 0)

        # li prendo dal database
        topics_from_db = db.get_all_topics()

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(topics_from_db, downloaded_topics, "Le due liste non corrispondono")

    def test_indicator(self):
        db = cache_db.CacheDB()
        # db.delete_all_indicators() # LENTO

        # li scarico
        topic = fetch.one_topic(3)  # Economy and Growth
        wb_indicators = fetch.all_indicators_from_topic(topic)

        # controllo che siano stati scaricati dati
        self.assertTrue(len(wb_indicators) > 0)

        # li prendo dal database
        db_indicators: List[Indicator] = db.get_indicators_from_topic(topic.topic_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(db_indicators, wb_indicators, "Le due liste non corrispondono")


if __name__ == '__main__':
    unittest.main()
