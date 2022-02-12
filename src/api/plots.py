from typing import List, Dict, Any, Tuple

from src.api import fetch
from src.wb.Observable import Observable
from src.wb.Plotter import Plotter
import src.wb.download_wb as dl


def new_multiple_observables_plot(indicator_country: List[Tuple[str, str]]) -> Any:
    """
    Crea un grafico con gli observables degli indicatori dati e delle nazioni/della nazione dati in input.
    :param indicator_country: Lista di tuple in cui il primo elemento è un id indicator
                              e il secondo la stringa della nazione
    :return: il plot da mostrare con .show()
    """
    plotter: Plotter = Plotter([{}])
    observable_list = []
    for (ind, country) in indicator_country:
        series: List[Observable] = fetch.all_observable_of_indicator(ind, country)
        observable_list.append((ind, country, series))
    return plotter.observables_plot_new(observable_list)


def three_obs(ind: List[str], country: List[str]):
    """Restituisce il grafico di un osservabile"""
    param_dict = []
    for i in range(len(ind)):
        all_observables = dl.download_observables_of_indicator(ind[i], country[i])
        # todo usare fetch.all_observable_of_indicator
        param_dict.append({"indicator": all_observables[0].indicator_id,
                           "country": all_observables[0].country,
                           "years": [],
                           "values": []
                           })
        for obs in all_observables:
            # insert 0 e non append perché i risultati vengono scaricati dal piu' recente al meno recente.
            param_dict[i].get("years").insert(0, obs.date)
            param_dict[i].get("values").insert(0, obs.value if obs.value is not None else 0)
            # TODO: METTERE NELLA RELAZIONE il fatto dei None
    plotter = Plotter(param_dict)
    return plotter.observable_plot()


def retta_reg(ind: str, country: str):
    """Restituisce la retta di regressione di un osservabile per una data nazione"""
    values = dl.download_observables_of_indicator(ind, country)  # todo usare fetch.all_observable_of_indicator
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    plotter = Plotter([param_dict])
    return plotter.retta_reg([])


def media_mobile(ind: str, country: str, win: int):
    """Istruzione cerca osservabili su db"""
    values = dl.download_observables_of_indicator(ind, country)  # todo usare fetch.all_observable_of_indicator
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    plotter = Plotter([param_dict])
    return plotter.media_mobile(w=win)


def media_mobile_new(ind: str, country: str, win: int):
    """
    Ricava il grafico media mobile di una serie di osservabili
    :param ind: id dell'indicatore
    :param country: nazione (Es. usa)
    :param win: dimensione della finestra per la media mobile
    :return: grafico media mobile della serie
    """
    plotter = Plotter([{}])
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.media_mobile_new(serie, win)
