import sqlite3
import logging
from sqlite3 import Connection
from typing import Optional

from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic

DB_NAME = "../resources/cache.db"


# I metodi che iniziano per '_' non dovrebbero essere chiamati dagli utenti che usano il package
class CacheDB:
    def __init__(self):
        """
        Costruttore di CacheDB. Inizializza la connessione al database e la salva in una variabile d'istanza.
        """
        self.conn: Connection = self._connect()

    def __del__(self):
        """
        Distruttore di CacheDB. Quando l'oggetto viene distrutto, si disconnette dal database
        :return:
        """
        self._disconnect()

    def _connect(self) -> Optional[Connection]:  # Optional[] serve solo a ricordare che la connessione può essere nulla
        """
        Prova a connettersi a un database cache.db. Se non esiste ne crea uno nuovo.
        :return: Connection or None
        """
        try:
            conn = sqlite3.connect(DB_NAME)
            logging.debug("Aperta la connessione")
            return conn
        except sqlite3.Error as e:
            logging.error(e)
        return None

    def _disconnect(self):
        """
        Disconnette il database, se non è stato chiuso. Viene chiamata anche dal distruttore.
        """
        if self.conn is not None:
            self.conn.close()
            logging.debug("Chiusa la connessione")

    def _save_observable(self, o: Observable):
        pass

    def _save_indicator(self, i: Indicator):
        pass

    def _save_topic(self, t: Topic):
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    CacheDB()
