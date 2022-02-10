import logging
from typing import List, Optional

import requests
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic

TOPIC_BASE_URL = 'https://api.worldbank.org/v2/topic'
FORMAT_INDICATOR_URL = TOPIC_BASE_URL + '/{}/indicator?format=json&per_page={}'
FORMAT_SINGLE_INDICATOR_URL = "http://api.worldbank.org/v2/indicators/{}?format=json"
FORMAT_OBSERVABLE_URL = 'https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&page=1&per_page={}'


def download_all_topics() -> List[Topic]:
    """
    Anche se permette di scaricare tutti i Topic WorldBank,
    l'utente dovrebbe utilizzare fetch.all_topics() perché sfrutta il database come cache
    :return:
    """
    # Scarico json dei topic
    r: requests.Response = requests.get(TOPIC_BASE_URL + '?format=json', allow_redirects=True)
    json_obj = r.json()[1]  # ricavo la lista di Topic Json dal contenuto della response

    all_topics: List[Topic] = []
    for json_topic in json_obj:
        all_topics.append(Topic(json_topic.get("id"),
                                json_topic.get("value"),
                                json_topic.get("sourceNote")))
    return all_topics


def download_indicators_for_topic(top: Topic) -> List[Indicator]:
    # Scarico json degli indicatori per topic
    r: requests.Response = requests.get(FORMAT_INDICATOR_URL.format(top.topic_id, 1),
                                        allow_redirects=True)

    # r: requests.Response = requests.get('{}/{}/indicator?format=json&per_page=1'.format(BASE_URL, t.id),
    #                                    allow_redirects=True)
    json_total = r.json()[0].get("total")

    r: requests.Response = requests.get(FORMAT_INDICATOR_URL.format(top.topic_id, json_total), allow_redirects=True)
    # r: requests.Response = requests.get(
    #     '{}/{}/indicator?format=json&page=1&per_page={}'.format(BASE_URL, t.id, json_object), allow_redirects=True)

    json_indicators = r.json()[1]
    all_indicators: List[Indicator] = []

    for json_indicator in json_indicators:
        topic: List[int] = [i.get("id") for i in json_indicator.get("topics")]
        all_indicators.append(Indicator(json_indicator.get("id"),
                                        json_indicator.get("name"),
                                        json_indicator.get("sourceNote"),
                                        topic))
    return all_indicators


def download_indicator(indicator_id: str) -> Optional[Indicator]:
    """
    Restituisce un unico indicator a partire dal suo identificativo testuale
    :param indicator_id: la stringa id dell'indicatore
    :return: un oggetto Indicator oppure None
    """
    r: requests.Response = requests.get(FORMAT_SINGLE_INDICATOR_URL.format(indicator_id), allow_redirects=True)
    json_total = r.json()[0].get("total")
    if json_total > 0:
        json_indicator = r.json()[1][0]
        Indicator(json_indicator.get("id"),
                  json_indicator.get("name"),
                  json_indicator.get("sourceNote"),
                  [i.get("id") for i in json_indicator.get("topics")])
    return None


def download_observables_of_indicator(i: str, country: str) -> List[Observable]:
    # Scarico json degli osservatori per indicatore e paese
    r: requests.Response = requests.get(FORMAT_OBSERVABLE_URL.format(country, i, 1),
                                        allow_redirects=True)
    json_total = r.json()[0].get("total")

    if json_total == 0:
        logging.warning("Attenzione non sono stati trovati osservabili per l'indicatore ", i)
        return []
    r: requests.Response = requests.get(FORMAT_OBSERVABLE_URL.format(country, i, json_total),
                                        allow_redirects=True)
    observables = r.json()[1]
    all_values: List[Observable] = []
    for json_observable in observables:
        all_values.append(Observable(json_observable.get("indicator").get("id"),
                                     json_observable.get("countryiso3code"),
                                     json_observable.get("date"),
                                     json_observable.get("value")))

    return all_values


if __name__ == "__main__":
    topic_array = download_all_topics()
    indicator_array = download_indicators_for_topic(topic_array[0])
    print(download_observables_of_indicator(indicator_array[0].indicator_id, "usa"))
