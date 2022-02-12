from typing import List, Dict, Any, Tuple

from src.api import fetch
from src.wb.Observable import Observable
from src.wb.Plotter import Plotter
import src.wb.download_wb as dl


def multi_observables_plot(indicator_country: List[Tuple[str, str]]) -> Any:
    """
    Crea un grafico con gli observables degli indicatori dati e delle nazioni/della nazione dati in input.
    :param indicator_country: Lista di tuple in cui il primo elemento è un id indicator
                              e il secondo la stringa della nazione
    :return: il plot da mostrare con .show()
    """
    plotter: Plotter = Plotter()
    observable_list = []
    for (ind, country) in indicator_country:
        series: List[Observable] = fetch.all_observable_of_indicator(ind, country)
        observable_list.append((ind, country, series))
    return plotter.multi_observables_plot(observable_list)


def retta_reg(ind: str, country: str):
    """Restituisce la retta di regressione di un osservabile per una data nazione"""
    plotter = Plotter()
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.regression_rect(serie)


def media_mobile(ind: str, country: str, win: int):
    """
    Ricava il grafico media mobile di una serie di osservabili
    :param ind: id dell'indicatore
    :param country: nazione (Es. usa)
    :param win: dimensione della finestra per la media mobile
    :return: grafico media mobile della serie
    """
    plotter = Plotter()
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.moving_avg(serie, win)
