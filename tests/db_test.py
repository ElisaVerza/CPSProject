import unittest

from src.opandas_wb.api.fetch import *
from src.opandas_wb.sqlite.cache_db import *


class DBTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.WARNING)
        self.db = CacheDB()

    def test_connection(self):  # i nomi dei metodi di test devono iniziare con "test"
        self.assertIsNotNone(self.db.conn)  # controllo che la connessione non sia None

    def test_observables(self):
        # prendo tutti gli osservabili dell'indicatore da world bank
        wb_obs = all_observable_of_indicator("AG.AGR.TRAC.NO", "usa")
        self.assertTrue(len(wb_obs) > 0)
        # prendo tutti gli osservabili dell'indicatore dal database
        db_obs = self.db.get_observables_of_indicator("AG.AGR.TRAC.NO", "usa")

        # controllo che siano presenti dati
        self.assertTrue(len(db_obs) > 0)

        # controllo che tutti gli osservabili di WB e DB siano gli stessi
        self.assertListEqual(wb_obs, db_obs)

    def test_topic(self):
        # CREATE: controllo se un topic è stato inserito correttamente
        self.db.save_all_topics([Topic(999, "Topic999", "Un topic 999")])
        topic = self.db.get_topic(999)  # READ
        self.assertIsNotNone(topic)

        # UPDATE topic
        self.db.update_topic(Topic(999, "Topic999 Modificato", "Un topic 999 modificato"))
        topic2 = self.db.get_topic(999)  # READ
        self.assertNotEqual(topic, topic2)

        # DELETE: controllo se un topic è stato eliminato correttamente
        self.db.delete_topic(999)
        topic_none = self.db.get_topic(999)  # READ
        self.assertIsNone(topic_none)

    def test_indicators(self):
        # CREATE: controllo se un topic è stato inserito correttamente
        self.db.save_all_indicators([Indicator("UNO", "Indicator Test", "Un Indicator Test", [3, 6, 9])])
        indicator = self.db.get_indicator("UNO")  # READ
        self.assertIsNotNone(indicator)

        # UPDATE topic
        self.db.update_indicator(Indicator("UNO", "Indicator Test Modificato", "Modifica Indicator Test", [3, 9]))
        indicator_mod = self.db.get_indicator("UNO")  # READ
        self.assertNotEqual(indicator, indicator_mod)

        # DELETE: controllo se un topic è stato eliminato correttamente
        self.db.delete_indicator("UNO")
        indicator_none = self.db.get_indicator("UNO")  # READ
        self.assertIsNone(indicator_none)


if __name__ == '__main__':
    unittest.main()
