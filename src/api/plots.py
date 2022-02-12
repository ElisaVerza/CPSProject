from typing import List, Any, Tuple

from src.api import fetch
from src.wb.Observable import Observable
from src.wb.Plotter import Plotter
import pandas as pd


def multi_observables_plot(indicator_country: List[Tuple[str, str]]) -> Any:
    """
    Crea un grafico con gli observables degli indicatori dati e delle nazioni/della nazione dati in input.
    :param indicator_country: Lista di tuple in cui il primo elemento è un id indicator
                              e il secondo la stringa della nazione di 3 caratteri (es. ita)
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
    :param country: stringa nazione di 3 caratteri (Es. usa, esp, ita)
    :param win: dimensione della finestra per la media mobile
    :return: grafico media mobile della serie
    """
    plotter = Plotter()
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.moving_avg(serie, win)


def diff_prime(ind: str, country: str):
    """
    Ricava il grafico delle differenze prime di una serie
    di osservabili appartenenti a un indicatore e di una nazione
    :param ind: id dell'indicatore da graficare
    :param country: stringa nazione di 3 caratteri (Es. usa)
    :return: grafico differenze prime della serie
    """
    plotter = Plotter()
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.diff_prime(serie, False)


def diff_prime_perc(ind: str, country: str):
    """
    Ricava il grafico delle differenze prime percentuali
    di una serie di osservabili appartenenti a un indicatore di una nazinoe
    :param ind: id dell'indicatore da graficare
    :param country: stringa nazione di 3 caratteri (Es. usa)
    :return: grafico differenze prime percentuali della serie
    """
    plotter = Plotter()
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.diff_prime(serie, True)


def covarianza(ind_country_x: Tuple[str, str], ind_country_y: Tuple[str, str]) -> float:
    """
    Ricava la covarianza degli osservabili di una serie
    :param ind: id dell'indicatore di cui calcolare la covarianza degli osservabili
    :param country: stringa nazione di 3 caratteri (Es. usa)
    :return: la covarianza degli osservabili
    """
    observables_x: List[Observable] = fetch.all_observable_of_indicator(ind_country_x[0], ind_country_x[1])
    observables_y: List[Observable] = fetch.all_observable_of_indicator(ind_country_y[0], ind_country_y[1])

    serie_x = pd.Series([o.value for o in observables_x if o.value is not None])
    serie_y = pd.Series([o.value for o in observables_y if o.value is not None])

    # media_campionaria_x = serie_x.mean()
    # media_campionaria_y = serie_y.mean()
    # n = serie_x.size
    # m = serie_y.size
    # covarianza = 1 / (n-1) * _sum_all(serie_x, media_campionaria)
    return serie_x.cov(serie_y)


def _sum_all(serie: pd.Series, media_campionaria) -> float:
    serie = (serie - media_campionaria) ** 2
    return serie.sum()


def prova_scatter_plot(ind_country_x: Tuple[str, str], ind_country_y: Tuple[str, str]):
    observables_x: List[Observable] = fetch.all_observable_of_indicator(ind_country_x[0], ind_country_x[1])
    observables_y: List[Observable] = fetch.all_observable_of_indicator(ind_country_y[0], ind_country_y[1])

    observables_x = [o for o in observables_x if o.value is not None]
    observables_y = [o for o in observables_y if o.value is not None]

    list_x: List[Observable] = []
    for i in range(len(observables_x)):
        # se l'anno di x è inclusa negli anni di y
        if observables_x[i].value is not None and observables_x[i].date in [o.date for o in observables_y]:
            list_x.append(observables_x[i])
    list_y: List[Observable] = []
    for i in range(len(observables_y)):
        # se l'anno di y è inclusa negli anni di x
        if observables_y[i].value is not None and observables_y[i].date in [o.date for o in observables_x]:
            list_y.append(observables_y[i])

    print("len(x) e len(y):", len(list_x), len(list_y))
    return Plotter().compare_dataset_scatter(list_x, list_y)


if __name__ == '__main__':
    covarianza()
