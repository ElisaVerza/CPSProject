from typing import List, Optional

from src.sqlite.cache_db import CacheDB
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic
from src.wb import download_wb


def one_topic(topic_id: int, force_update=False) -> Optional[Topic]:
    """
    Ricava un topic dato il suo id. Se possibile lo prende dal database, altrimenti lo scarica da WorldBank
    :return: il topic richiesto
    """
    db = CacheDB()  # mi connetto al database

    if not force_update:
        # provo a prendere tutti i topic dal database
        topic = db.get_topic(topic_id)

        # se trovo almeno un topic restituisco la lista
        if topic is not None:
            return topic

    # se non trovo niente, scarico da WorldBank
    topic = download_wb.download_topic(topic_id)
    # ... e aggiorno il database (se un topic già era presente, lo sostituisce)
    db.save_all_topics([topic])
    return topic

    # the_topics = all_topics(force_update)
    # # Alternativa al for: prende il primo topic con id dato in input tra gli all_topics, altrimenti None.
    # return next(filter(lambda top: top.topic_id == topic_id, the_topics), None)


def all_topics(force_update=False) -> List[Topic]:
    """
    Permette di prendere tutti i topic. Se non sono ancora stati scaricati, li scarica
    da WorldBank e poi li salva nel database, altrimenti li prende direttamente dal database
    :param force_update: se True, scarica sempre da WorldBank e poi aggiorna il database
    :return: la lista di topic presa dal database
    """
    db = CacheDB()  # mi connetto al database

    if not force_update:
        # provo a prendere tutti i topic dal database
        topic_list = db.get_all_topics()

        # se trovo almeno un topic restituisco la lista
        if len(topic_list) > 0:
            return topic_list

    # se non trovo niente, scarico da WorldBank
    topic_list = download_wb.download_all_topics()
    # ... e aggiorno il database (se un topic già era presente, lo sostituisce)
    db.save_all_topics(topic_list)
    return topic_list


def one_indicator(indicator_id: str, force_update=False) -> Optional[Indicator]:
    db = CacheDB()

    if not force_update:
        # provo a cercare l'indicator nel database
        indic = db.get_indicator(indicator_id)
        if indic is not None:
            return indic
    indic = download_wb.download_indicator(indicator_id)
    db.save_all_indicators([indic])
    return indic


def all_indicators_from_topic(topic: Topic, force_update=False) -> List[Indicator]:
    db = CacheDB()  # mi connetto al database

    if not force_update:
        # provo a prendere tutti i topic dal database
        indicator_list = db.get_indicators_from_topic(topic.topic_id)

        # se trovo almeno un topic restituisco la lista
        if len(indicator_list) > 0:
            return indicator_list

    # se non trovo niente, scarico da WorldBank
    indicator_list = download_wb.download_indicators_for_topic(topic)
    # ... e aggiorno il database (se un topic già era presente, lo sostituisce)
    db.save_all_indicators(indicator_list)
    return indicator_list


def all_observable_of_indicator(indicator_id: str, country: str, force_update=False) -> List[Observable]:
    lista: List[Observable] = download_wb.download_observables_of_indicator(indicator_id, country)
    lista.sort(key=lambda o: o.date, reverse=False)
    return lista


if __name__ == '__main__':
    print(all_topics())
