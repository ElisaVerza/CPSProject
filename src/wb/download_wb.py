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


def get_indicator_for_topic(t: Topic) -> Indicator:
    return None


def get_observables_of_indicator(i: Indicator) -> Observable:
    return None


if __name__ == "__main__":
    get_all_topics()
