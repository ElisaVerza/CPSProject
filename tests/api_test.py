import logging
import unittest
from typing import List

from src.api import fetch
from src.sqlite import cache_db
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable


class ApiTestCase(unittest.TestCase):
    """
    Attenzione: Tutti i test di questa classe richiedono connessione a internet!
    """

    def setUp(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.db = cache_db.CacheDB()

    def test_topic(self):
        # elimino e rimetto un topic
        self.db.delete_topic(1)
        wb_topic = fetch.one_topic(1)
        db_topic = self.db.get_topic(1)
        self.assertIsNotNone(wb_topic)
        self.assertEqual(wb_topic, db_topic, "I due topic non coincidono")

    def test_all_topics(self):
        # scarico e aggiorno i topics nel db
        downloaded_topics = fetch.all_topics(force_update=True)

        # controllo che siano stati scaricati dati
        self.assertTrue(len(downloaded_topics) > 0, "Impossibile scaricare i topics. Controlla la connessione internet")

        # li prendo dal database
        topics_from_db = self.db.get_all_topics()

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(topics_from_db, downloaded_topics, "Le due liste non corrispondono")

    def test_indicator(self):
        ind_id = 'AG.AGR.TRAC.NO'

        # scarico o prendo dal DB un indicator
        wb_indicator = fetch.one_indicator(ind_id)

        # controllo che siano stati scaricati dati
        self.assertIsNotNone(wb_indicator, "Impossibile scaricare l'indicatore. Controlla la connessione internet")

        # li prendo dal database
        db_indicator: Indicator = self.db.get_indicator(ind_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertEqual(db_indicator, wb_indicator, "I due Indicator non corrispondono")

    def test_indicator_from_topic(self):
        # Prendo da WB un topic e tutti gli indicator che riguardano quel topic
        topic = fetch.one_topic(1)  # 3 Economy and Growth
        wb_indicators = fetch.all_indicators_from_topic(topic, force_update=True)

        # controllo che siano stati scaricati dati
        self.assertTrue(len(wb_indicators) > 0, "Impossibile scaricare l'indicatore. Controlla la connessione internet")

        # li prendo dal database
        db_indicators: List[Indicator] = self.db.get_indicators_from_topic(topic.topic_id)

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(db_indicators, wb_indicators, "Le due liste non corrispondono")

    def test_observable(self):
        # Prendo da WB un topic e tutti gli indicator che riguardano quel topic
        topic = fetch.one_topic(1)  # Agriculture
        indicators = fetch.all_indicators_from_topic(topic, force_update=True)
        # scarico gli osservabili di un indicatore
        wb_observables = fetch.all_observable_of_indicator(indicators[0].indicator_id, 'usa')

        # controllo che siano stati scaricati dati
        self.assertTrue(len(wb_observables) > 1, "Impossibile scaricare almeno 2 osservabili. Controlla internet")
        self.assertTrue(wb_observables[0].date < wb_observables[1].date)

        # li prendo dal database
        db_observables: List[Observable] = self.db.get_observables_of_indicator(indicators[0].indicator_id, "usa")

        # verifico che i dati siano uguali
        # (chiamano il metodo __eq__, attenzione agli interi: vengono trasformati in stringa)
        self.assertListEqual(db_observables, wb_observables, "Le due liste non corrispondono")


if __name__ == '__main__':
    unittest.main()
