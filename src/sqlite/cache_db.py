import os
import pathlib
import sqlite3
import logging
from sqlite3 import Connection
from typing import Optional, List

from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic

DB_NAME = "../resources/cache.db"
CREATE_TABLE_FILE = "../resources/create_tables.sql"


# def db_exists(db_name: str) -> bool:
#     return os.path.exists(pathlib.Path(db_name))


# I metodi che iniziano per '_' non dovrebbero essere chiamati dagli utenti che usano il package
class CacheDB:
    def __init__(self):
        """
        Costruttore di CacheDB. Inizializza la connessione al database e la salva in una variabile d'istanza.
        """
        self._connect()

    def __del__(self):
        """
        Distruttore di CacheDB. Prima di distruggere l'oggetto, si disconnette dal database
        :return:
        """
        self._disconnect()

    def _connect(self):
        """
        Prova a connettersi a un database cache.db. Se non esiste ne crea uno nuovo.
        :return: Connection or None
        """
        try:
            self.conn = sqlite3.connect(DB_NAME)
            logging.debug("Aperta la connessione con il cache db")
            self._create_tables_if_not_exist()  # creo le tabelle, se ancora non esistono
        except sqlite3.Error as e:
            logging.error(e)
            self.conn = None

    def _create_tables_if_not_exist(self):
        """
        Crea le tabelle del database cache
        """
        # Apro un cursore
        cursor = self.conn.cursor()

        # Apro il file che permette di creare le tabelle
        file = open(CREATE_TABLE_FILE, 'r')

        # Eseguo lo script SQL contenuto nel file
        cursor.executescript(file.read())

        # Eseguo il Commit dell'operazione
        self.conn.commit()

        # Chiudo il cursore.
        cursor.close()

    def _disconnect(self):
        """
        Disconnette il database, se non è stato chiuso. Viene chiamata anche dal distruttore.
        """
        if self.conn is not None:
            self.conn.close()
            logging.debug("Chiusa la connessione con il cache db")

    def save_all_topics(self, all_topics: List[Topic]):
        """
        Salva una lista di topic nel database
        :param t: l'oggetto Topic da salvare
        """
        cursor = self.conn.cursor()
        try:
            sql_insert_with_3_params = open("../resources/insert_all_topics.sql").read()
            for topic in all_topics:
                cursor.execute(sql_insert_with_3_params, topic.to_tuple())
        except sqlite3.Error as error:
            logging.error("Impossibile inserire i topics: ", error)
        finally:
            cursor.close()

    def save_indicator(self, i: Indicator):
        """
        Salva un indicator nel database
        :param i: l'oggetto Indicator da salvare
        """
        pass

    def save_observable(self, o: Observable):
        pass

    def get_topic(self, id: int) -> Optional[Topic]:  # Optional[] serve solo a ricordare che il Topic può essere None
        """
        Cerca un Topic da un database, se presente
        :param id: l'id del topic da cercare
        :return: un oggetto Topic, oppure None
        """
        cursor = self.conn.cursor()
        try:
            sql_get_topic = open("../resources/get_topic.sql").read()
            cursor.execute(sql_get_topic, id)
            topic_tuple = cursor.fetchone()
            return Topic(topic_tuple[0], topic_tuple[1], topic_tuple[2])
        except sqlite3.Error as error:
            logging.error("Impossibile inserire i topics: ", error)
        finally:
            cursor.close()

    def get_indicator(self, id: int) -> Optional[Indicator]:
        pass

    def get_observable(self, id: int) -> Optional[Observable]:
        pass

    def remove_topic(self, id: int):
        cursor = self.conn.cursor()
        try:
            sql_remove_topic = open("../resources/remove_topic.sql").read()
            cursor.execute(sql_remove_topic, id)
        except sqlite3.Error as error:
            logging.error("Impossibile inserire i topics: ", error)
        finally:
            cursor.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    CacheDB()
