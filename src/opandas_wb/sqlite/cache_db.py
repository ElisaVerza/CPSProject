import sqlite3
import logging

from sqlite3 import Connection
from typing import Optional, List, Dict, Tuple
from . import constants as const
from ..wb.Indicator import Indicator
from ..wb.Observable import Observable
from ..wb.Topic import Topic
from ..wb.interface import IWbObject


# I metodi che iniziano per '_' non dovrebbero essere chiamati dagli utenti che usano il package
class CacheDB:
    """
    Questa classe permette di gestire il database cache per i dati scaricati da WorldBank (Observable, Indicator, Topic)
    """

    def __init__(self, name=const.DB_NAME):
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
        cursor.executescript(const.CREATE_TABLE_QUERY)

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

    def _save_one(self, insert_str: str, object_tuple: Tuple):
        """
        Salva un oggetto generico nel database
        :param insert_str: query INSERT o REPLACE
        :param object_tuple: argomento della query
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(insert_str, object_tuple)
            self.conn.commit()
        except sqlite3.Error as error:
            logging.error("Impossibile eseguire la query di inserimento ", insert_str, error)
        finally:
            self.conn.commit()
            cursor.close()

    def _save_all(self, insert_str: str, all_objects: List):
        """
        Salva una lista di oggetti generici nel database
        :param insert_str: query INSERT o REPLACE
        :param all_objects: lista di tuple che rappresentano gli oggetti oppure oggetti IWbObject
        """
        cursor = self.conn.cursor()
        try:
            for o in all_objects:
                if isinstance(o, IWbObject):
                    cursor.execute(insert_str, o.to_tuple())
                else:
                    cursor.execute(insert_str, o)
            self.conn.commit()
        except sqlite3.Error as error:
            logging.error("Impossibile eseguire la query di inserimento ", insert_str, error)
        finally:
            self.conn.commit()
            cursor.close()

    def _get_one(self, query_str: str, query_arg: Dict) -> Tuple:
        """
        Ricava una riga dal database
        :param query_str: query di select
        :param query_arg: argomento della query
        :return: tupla che rappresenta la riga
        """
        cursor = self.conn.cursor()
        result = None
        try:
            cursor.execute(query_str, query_arg)
            result = cursor.fetchone()
        except sqlite3.Error as error:
            logging.error("Query fallita: ", query_str + str(query_arg), error)
        except TypeError:
            result = None
        finally:
            self.conn.commit()
            cursor.close()
        return result

    def _get_all(self, query_str: str, arg=None) -> List[Tuple]:
        """
        Esegue una query generica
        :param query_str: query di select
        :param arg: argomento della query
        :return: tupla che rappresenta la riga
        """
        cursor = self.conn.cursor()
        result = []
        try:
            if arg is not None:
                cursor.execute(query_str, arg)
            else:
                cursor.execute(query_str)
            result = cursor.fetchall()
        except sqlite3.Error or TypeError as error:
            logging.error("Query fallita: ", query_str, error)
        finally:
            self.conn.commit()
            cursor.close()
        return result

    def _update_one(self, update_str: str, object_tuple: Tuple):
        """
        Aggiorna una riga generica
        :param update_str: query di aggiornamento
        :param object_tuple: tupla di aggiornamento
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(update_str, object_tuple)
        except sqlite3.Error as error:
            logging.error("Impossibile aggiornare: ", update_str + str(object_tuple), error)
        finally:
            self.conn.commit()
            cursor.close()

    def _update_all(self, update_str: str, all_object: List):
        """
        Aggiorna una tabella con tutti gli oggetti nella lista
        :param update_str: stringa di UPDATE
        :param all_object: tutti gli oggetti da aggiornare
        """
        cursor = self.conn.cursor()
        try:
            for o in all_object:
                o = o.to_tuple()
                o = o + o[:3]
                cursor.execute(update_str, o)
        except sqlite3.Error as error:
            logging.error("Impossibile aggiornare: ", update_str + str(all_object), error)
        finally:
            self.conn.commit()
            cursor.close()

    def _remove(self, remove_str: str, remove_arg: Dict):
        """
        Esegue una query di remove (puo' eliminare anche piu' di una riga, dipende dalla query).
        :param remove_str: la query di remove con un argomento
        :param remove_arg: l'argomento della query di remove
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(remove_str, remove_arg)
        except sqlite3.Error as error:
            logging.error("Impossibile eliminare: ", remove_str + str(remove_arg), error)
        finally:
            self.conn.commit()
            cursor.close()

    def _truncate(self, table: str):
        """
        Elimina tutti i contenuti di una tabella
        :param table: il nome della tabella
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM {} WHERE TRUE".format(table))
        except sqlite3.Error as error:
            logging.error("Impossibile eliminare tutti i topics: ", error)
        finally:
            self.conn.commit()
            cursor.close()

    def save_all_topics(self, all_topics: List[Topic]):
        """
        Salva una lista di topic nel database. Se un topic e' gia' presente, lo sostituisce
        :param all_topics: la lista di oggetti Topic da salvare
        """
        self._save_all(const.INSERT_ALL_TOPICS, all_topics)

    def save_all_indicators(self, all_indicators: List[Indicator]):
        """
        Salva la lista di oggetti Indicators nel database
        :param all_indicators: la lista da salvare
        """
        self._save_all(const.INSERT_INDICATORS, all_indicators)
        for indicator in all_indicators:
            indicator_topics = indicator.indicator_topic_list()
            for row in indicator_topics:
                self._save_one(const.INSERT_INDICATOR_TOPICS, row)

    def save_observable(self, o: List[Observable]):
        """
        Salva gli observable della lista nel database
        :param o: lista di osservabili da salvare
        """
        self._save_all(const.INSERT_OBSERVABLES, o)

    def get_topic(self, topic_id: int) -> Optional[Topic]:  # Optional[] serve a ricordare che il Topic può essere None
        """
        Cerca un Topic dal database, se presente
        :param topic_id: l'id del topic da cercare
        :return: un oggetto Topic, oppure None
        """
        topic = self._get_one(const.GET_TOPIC, {"topic_id": topic_id})
        if topic is not None:
            return Topic(int(topic[0]), topic[1], topic[2])
        return None

    def get_all_topics(self) -> List[Topic]:
        """
        Ricava tutti i topic presenti nel database
        :return: la lista di topic nel database, potrebbe essere vuota.
        """
        topic_tuples = self._get_all(const.GET_ALL_TOPICS)
        topic_list = []
        for topic_tup in topic_tuples:
            topic_list.append(Topic(int(topic_tup[0]), topic_tup[1], topic_tup[2]))
        return topic_list

    def get_indicator(self, indicator_id: str) -> Optional[Indicator]:
        """
        Cerca un Indicator nel database, a partire dal suo id
        :param indicator_id: id dell'indicator
        :return: l'oggetto Indicator oppure None
        """
        ind_without_topics: Tuple[str, str, str] = self._get_one(const.GET_INDICATOR, {"indicator_id": indicator_id})
        ind_topics: List[Tuple[int]] = self._get_all(const.GET_INDICATOR_TOPICS, arg={"indicator_id": indicator_id})
        if ind_without_topics is not None:
            topic_list: List[int] = []
            for tuples in ind_topics:
                topic_list.append(tuples[0])
            return Indicator(ind_without_topics[0], ind_without_topics[1], ind_without_topics[2], topic_list)
        return None

    def get_indicators_from_topic(self, topic_id: int) -> List[Indicator]:
        """
        Cerca tutti gli Indicator nel database che appartengono a un certo topic
        :param topic_id: id del topic a cui appartiene l' Indicator
        :return: la lista degli Indicator trovati
        """
        indicators: List[Tuple[str]] = self._get_all(const.GET_INDICATORS_FROM_TOPIC_ID, arg={"topic_id": topic_id})
        indicator_list = []
        for indicator_id_tuple in indicators:
            indicator_list.append(self.get_indicator(indicator_id_tuple[0]))
        return indicator_list

    def get_observables_of_indicator(self, indicator_id: str, country: str = None) -> List[Observable]:
        """
        Cerca tutti gli Observables nel database di un indicatore relativo ad un paese
        se country è specificato, altrimenti restituisce tutti gli Observables di un indicatore
        :param indicator_id: id dell'indicatore
        :param country: paese di interesse
        :return: la lista degli Observable trovati
        """
        observables_list: List[Observable] = []
        observables: List[Tuple[str]]
        if country is not None:
            observables = self._get_all(const.GET_OBSERVABLES_COUNTRY,
                                        arg={"obs_ind_id": indicator_id, "country": country})
        else:
            observables = self._get_all(const.GET_OBSERVABLES,
                                        arg={"obs_ind_id": indicator_id})

        for indicator_id_tuple in observables:
            observables_list.append(Observable(indicator_id_tuple[0],
                                               indicator_id_tuple[1],
                                               indicator_id_tuple[2],
                                               indicator_id_tuple[3]))
        return observables_list

    def delete_topic(self, topic_id: int):
        """
        Elimina un topic dal database dato il suo id, se presente
        :param topic_id: l'id del topic da rimuovere
        """
        self._remove(const.REMOVE_TOPIC, {"topic_id": topic_id})

    def delete_all_topics(self):
        """
        Elimina tutti i topics dal database. Usare con cautela.
        """
        self._truncate("topics")

    def delete_indicator(self, indicator_id: str):
        """
        Elimina un indicator e i suoi topic
        :param indicator_id: l'id dell' Indicator
        """
        self._remove(const.REMOVE_INDICATOR_TOPICS, {"indicator_id": indicator_id})
        self._remove(const.REMOVE_INDICATOR, {"indicator_id": indicator_id})

    def delete_all_indicators(self):
        """
        Elimina tutti gli indicatori dal database. Usare con cautela.
        """
        self._truncate("indicator_topics")
        self._truncate("indicators")

    def delete_observable(self, obs_ind_id: str, country: str = None):
        """
        Elimina tutti gli Observables di un indicatore e se specificato il paramentro country
        elimina tutti gli Observables di un indicatore di un determinato paese
        :param obs_ind_id: id dell'indicatore
        :param country: paese di interesse
        """
        if country is not None:
            self._remove(const.REMOVE_OBSERVABLES_COUNTRY, {"obs_ind_id": obs_ind_id, "country": country})
        else:
            self._remove(const.REMOVE_OBSERVABLES, {"indicator_id": obs_ind_id})

    def delete_all_observables(self):
        """
        Elimina tutti gli osservabili dal database. Usare con cautela.
        """
        self._truncate("observables")

    def update_topic(self, t: Topic):
        """
        Aggiorna un singolo topic nel database, se presente.
        :param t: l'oggetto Topic che si vuole aggiornare
        """
        self._update_one(const.UPDATE_TOPIC, (t.value, t.sourceNote, t.topic_id))

    def update_indicator(self, i: Indicator):
        """
        Aggiorna un indicator (e i suoi Topic) nel database, se presente.
        :param i: l'oggetto Indicator che si vuole aggiornare
        """
        self._update_one(const.UPDATE_INDICATOR, (i.name, i.sourceNote, i.indicator_id))
        self._remove(const.REMOVE_INDICATOR_TOPICS, {"indicator_id": i.indicator_id})
        self._save_all(const.INSERT_INDICATOR_TOPICS, i.indicator_topic_list())

    def update_observable(self, o: List[Observable]):
        """
        Aggiorna una lista di osservabili
        :param o: lista di osservabili
        """
        self._update_all(const.UPDATE_OBSERVABLES, o)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    CacheDB()
