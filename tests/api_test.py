import unittest
from typing import List

from src.api import fetch
from src.sqlite import cache_db
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable


class ApiTestCase(unittest.TestCase):
    def test_topic(self):
        db = cache_db.CacheDB()
        db.delete_topic(1)

        wb_topic = fetch.one_topic(1)
        db_topic = db.get_topic(1)
        self.assertIsNotNone(wb_topic)
        self.assertEqual(wb_topic, db_topic, "I due topic non coincidono")

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
        ind_id = 'AG.AGR.TRAC.NO'
        db.delete_indicator(ind_id)  # LENTO

        # li scarico
        wb_indicator = fetch.one_indicator(ind_id)
        print(wb_indicator, wb_indicator.topics)
        # controllo che siano stati scaricati dati
        self.assertIsNotNone(wb_indicator)

        # li prendo dal database
        db_indicator: Indicator = db.get_indicator(ind_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertEqual(db_indicator, wb_indicator, "I due Indicator non corrispondono")

    def test_indicator_from_topic(self):
        db = cache_db.CacheDB()
        # db.delete_all_indicators() # LENTO

        # li scarico
        topic = fetch.one_topic(1)  # 3 Economy and Growth
        wb_indicators = fetch.all_indicators_from_topic(topic)

        # controllo che siano stati scaricati dati
        self.assertTrue(len(wb_indicators) > 0)

        # li prendo dal database
        db_indicators: List[Indicator] = db.get_indicators_from_topic(topic.topic_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(db_indicators, wb_indicators, "Le due liste non corrispondono")

    def test_observable(self):
        db = cache_db.CacheDB()
        # db.delete_all_observables()  # LENTO

        topic = fetch.one_topic(1)  # Agriculture
        indicators = fetch.all_indicators_from_topic(topic)
        # li scarico
        wb_observables = fetch.all_observable_of_indicator(indicators[0].indicator_id, 'usa')
        print(indicators[0])

        # controllo che siano stati scaricati dati
        self.assertTrue(len(wb_observables) > 1)
        self.assertTrue(wb_observables[0].date < wb_observables[1].date)

        # li prendo dal database
        db_observables: List[Observable] = db.get_observables_of_indicator(indicators[0].indicator_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(db_observables, wb_observables, "Le due liste non corrispondono")


if __name__ == '__main__':
    unittest.main()
