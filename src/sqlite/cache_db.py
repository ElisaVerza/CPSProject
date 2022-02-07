import os
import sqlite3
import logging
from sqlite3 import Connection
from typing import Optional, List

from src.sqlite.constants import *
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic


# def db_exists(db_name: str) -> bool:
#     return os.path.exists(pathlib.Path(db_name))


# I metodi che iniziano per '_' non dovrebbero essere chiamati dagli utenti che usano il package
class CacheDB:
    """
    Questa classe permette di gestire il database cache per i dati scaricati da WorldBank (Observable, Indicator, Topic)
    """

    def __init__(self, name=DB_NAME):
        """
        Costruttore di CacheDB. Inizializza la connessione al database e la salva in una variabile d'istanza.
        """
        self.conn = self._connect(name)
        self._create_tables_if_not_exist()  # creo le tabelle, se ancora non esistono

    def __del__(self):
        """
        Distruttore di CacheDB. Prima di distruggere l'oggetto, si disconnette dal database
        """
        self._disconnect()

    def _connect(self, name: str) -> Optional[Connection]:
        """
        Prova a connettersi a un database cache.db. Se non esiste ne crea uno nuovo.
        :return: Connection o None
        """
        conn = None
        try:
            conn = sqlite3.connect(name)
            logging.debug("Aperta la connessione con il cache db")
        except sqlite3.Error as e:
            logging.error(e)
        return conn

    def _create_tables_if_not_exist(self):
        """
        Crea le tabelle del database cache
        """
        # Apro un cursore
        cursor = self.conn.cursor()

        # Eseguo lo script SQL contenuto nel file
        cursor.executescript(CREATE_TABLE_QUERY)

        # Eseguo il Commit dell'operazione
        self.conn.commit()

        # Chiudo il cursore.
        cursor.close()
        logging.debug("Create tabelle")

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
        :param all_topics: l'oggetto Topic da salvare
        """
        cursor = self.conn.cursor()
        try:
            for topic in all_topics:
                cursor.execute(INSERT_ALL_TOPICS, topic.to_tuple())
            self.conn.commit()
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

    def get_topic(self, topic_id: int) -> Optional[Topic]:  # Optional[] serve a ricordare che il Topic può essere None
        """
        Cerca un Topic da un database, se presente
        :param topic_id: l'id del topic da cercare
        :return: un oggetto Topic, oppure None
        """
        cursor = self.conn.cursor()
        topic = None
        try:
            cursor.execute(GET_TOPIC, {"topic_id": topic_id})
            topic_tuple = cursor.fetchone()
            topic = Topic(topic_tuple[0], topic_tuple[1], topic_tuple[2])  # topic_tuple puo essere nulla
        except sqlite3.Error as error:
            logging.error("Impossibile inserire i topics: ", error)
        except TypeError:
            topic = None
        finally:
            self.conn.commit()
            cursor.close()
        return topic

    def get_indicator(self, id: int) -> Optional[Indicator]:
        pass

    def get_observable(self, id: int) -> Optional[Observable]:
        pass

    def delete_topic(self, topic_id: int):
        cursor = self.conn.cursor()
        try:
            cursor.execute(REMOVE_TOPIC, {"topic_id": topic_id})
        except sqlite3.Error as error:
            logging.error("Impossibile inserire i topics: ", error)
        finally:
            cursor.close()

    def delete_indicator(self, obs_id: int):
        pass

    def delete_observable(self, obs_id: int):
        pass

    def update_topic(self, t: Topic):
        pass

    def update_indicator(self, i: Indicator):
        pass

    def update_observable(self, o: Observable):
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    CacheDB()
