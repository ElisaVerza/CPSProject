import logging
from typing import List, Optional

import requests
from opandas_wb.wb.Indicator import Indicator
from opandas_wb.wb.Observable import Observable
from opandas_wb.wb.Topic import Topic

TOPIC_BASE_URL = 'https://api.worldbank.org/v2/topic'
FORMAT_INDICATOR_URL = TOPIC_BASE_URL + '/{}/indicator?format=json&per_page={}'
FORMAT_SINGLE_INDICATOR_URL = "https://api.worldbank.org/v2/indicators/{}?format=json"
FORMAT_OBSERVABLE_URL = 'https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&page=1&per_page={}'


def download_topic(topic_id: int) -> Optional[Topic]:
    try:
        r: requests.Response = requests.get(TOPIC_BASE_URL + '?id={}&format=json'.format(topic_id),
                                            allow_redirects=True)

        if int(r.json()[0].get("total")) == 1:
            json_topic = r.json()[1][0]  # ricavo il Topic Json dal contenuto della response
            return Topic(int(json_topic.get("id")), json_topic.get("value"), json_topic.get("sourceNote"))
    except Exception as e:
        logging.warning("Errore: {}".format(e))
        return None


def download_all_topics() -> List[Topic]:
    """
    Anche se permette di scaricare tutti i Topic WorldBank,
    l'utente dovrebbe utilizzare fetch.all_topics() perché sfrutta il database come cache
    :return:
    """
    try:
        # Scarico json dei topic
        r: requests.Response = requests.get(TOPIC_BASE_URL + '?format=json', allow_redirects=True)
        json_obj = r.json()[1]  # ricavo la lista di Topic Json dal contenuto della response

        all_topics: List[Topic] = []
        for json_topic in json_obj:
            all_topics.append(Topic(int(json_topic.get("id")),
                                    json_topic.get("value"),
                                    json_topic.get("sourceNote")))
        return all_topics
    except Exception as e:
        logging.warning("Errore: {}".format(e))
        return []


def download_indicators_for_topic(top: Topic) -> List[Indicator]:
    try:
        # Scarico json degli indicatori per topic
        r: requests.Response = requests.get(FORMAT_INDICATOR_URL.format(top.topic_id, 1), allow_redirects=True)

        json_total = r.json()[0].get("total")

        r: requests.Response = requests.get(FORMAT_INDICATOR_URL.format(top.topic_id, json_total), allow_redirects=True)

        json_indicators = r.json()[1]
        all_indicators: List[Indicator] = []

        for json_indicator in json_indicators:
            topic: List[int] = [int(i.get("id")) for i in json_indicator.get("topics")]
            all_indicators.append(Indicator(json_indicator.get("id"),
                                            json_indicator.get("name"),
                                            json_indicator.get("sourceNote"),
                                            topic))
        return all_indicators
    except Exception as e:
        logging.warning("Errore: {}".format(e))
        return []


def download_indicator(indicator_id: str) -> Optional[Indicator]:
    """
    Restituisce un unico indicator a partire dal suo identificativo testuale
    :param indicator_id: la stringa id dell'indicatore
    :return: un oggetto Indicator oppure None
    """
    try:
        r: requests.Response = requests.get(FORMAT_SINGLE_INDICATOR_URL.format(indicator_id), allow_redirects=True)
        json_total = r.json()[0].get("total")
        if json_total > 0:
            json_indicator = r.json()[1][0]
            return Indicator(json_indicator.get("id"),
                             json_indicator.get("name"),
                             json_indicator.get("sourceNote"),
                             [int(i.get("id")) for i in json_indicator.get("topics")])
    except Exception as e:
        logging.warning("Errore: {}".format(e))
        return None


def download_observables_of_indicator(i: str, country: str) -> List[Observable]:
    # Scarico json degli osservatori per indicatore e paese
    try:
        r: requests.Response = requests.get(FORMAT_OBSERVABLE_URL.format(country, i, 1), allow_redirects=True)
        json_total = r.json()[0].get("total")

        if json_total == 0:
            logging.warning("Attenzione non sono stati trovati osservabili per l'indicatore ", i)
            return []
        r: requests.Response = requests.get(FORMAT_OBSERVABLE_URL.format(country, i, json_total), allow_redirects=True)
        observables = r.json()[1]

        all_values: List[Observable] = []
        for json_observable in observables:
            val = json_observable.get("value")
            if val is not None:
                val = float(val)
            all_values.append(Observable(json_observable.get("indicator").get("id"),
                                         str(json_observable.get("countryiso3code")).lower(),
                                         int(json_observable.get("date")),
                                         val))
        return all_values
    except Exception as e:
        logging.warning("Errore: {}".format(e))
        return []
