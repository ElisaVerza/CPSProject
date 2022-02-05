from time import sleep

import requests
import json


class DataAnalysis:

    def download(self):
        # Scarico json dei topic
        url_base = 'http://api.worldbank.org/v2/topic'
        r = requests.get(url_base + '?format=json', allow_redirects=True)
        j_obj = r.json()

        # Estraggo gli indicatori dai topic
        for i in range(1, len(j_obj[1]) + 1):
            # download file json indicatori per topic.
            r = requests.get(url_base + '/' + str(i) + '/indicator?format=json&per_page=1', allow_redirects=True)
            sleep(0.5)
            json_object = r.json()
            tot = json_object[0].get("total")
            print(tot)
            r = requests.get(url_base + '/' + str(i) + '/indicator?format=json&page=1&per_page=' + str(tot),
                             allow_redirects=True)
            json_object = r.json()
            with open('../resources/indicator' + str(i).zfill(2) + 'topic.json', 'w', encoding='utf-8') as f:
                json.dump(json_object, f)
        return


if __name__ == "__main__":
    DataAnalysis().download()
