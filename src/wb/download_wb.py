import json
from typing import List

import requests
from time import sleep
from src.wb.Indicator import Indicator
from src.wb.Observable import Observable
from src.wb.Topic import Topic

BASE_URL = 'http://api.worldbank.org/v2/topic'


def get_all_topics() -> List[Topic]:
    # Scarico json dei topic
    r: requests.Response = requests.get(BASE_URL + '?format=json', allow_redirects=True)
    json_obj = r.json()[1]  # ricavo la lista di Topic Json dal contenuto della response

    all_topics: List[Topic] = []
    for json_topic in json_obj:
        all_topics.append(Topic(json_topic.get("id"),
                                json_topic.get("value"),
                                json_topic.get("sourceNote")))
    return all_topics


def get_indicator_for_topic(t: Topic) -> List[Indicator]:
    # Scarico json degli indicatori per topic
    r: requests.Response = requests.get('{}/{}/indicator?format=json&per_page=1'.format(BASE_URL, t.id),
                                        allow_redirects=True)
    json_object = r.json()[0].get("total")

    r: requests.Response = requests.get(
        '{}/{}/indicator?format=json&page=1&per_page={}'.format(BASE_URL, t.id, json_object), allow_redirects=True)

    json_object = r.json()[1]
    all_indicators: List[Indicator] = []

    for json_indicator in json_object:
        topic: List[int] = [i.get("id") for i in json_indicator.get("topics")]
        all_indicators.append(Indicator(json_indicator.get("id"),
                                        json_indicator.get("name"),
                                        json_indicator.get("sourceNote"),
                                        topic))
    return all_indicators


def get_observables_for_indicator(i: Indicator, country: str):
    # Scarico json degli osservatori per indicatore e paese
    r: requests.Response = requests.get(
        'http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&per_page=1'.format(country, i.id),
        allow_redirects=True)
    json_object = r.json()[0].get("total")

    r: requests.Response = requests.get(
        'http://api.worldbank.org/v2/country/{}/indicator/{}?format=json&per_page={}'.format(country, i.id, json_object),
        allow_redirects=True)
    json_object = r.json()[1]
    all_values: List[Observable] = []
    for json_observable in json_object:
        all_values.append(Observable(json_observable.get("indicator").get("id"),
                                        json_observable.get("countryiso3code"),
                                        json_observable.get("date"),
                                        json_observable.get("value")))

    return all_values


if __name__ == "__main__":
    topic_array = get_all_topics()
    indicator_array = get_indicator_for_topic(topic_array[0])
    get_observables_for_indicator(indicator_array[0], "usa")
