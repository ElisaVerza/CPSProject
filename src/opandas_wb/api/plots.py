from typing import List, Any, Tuple

from . import fetch
from ..wb.Observable import Observable
from ..wb import plotter
import pandas as pd


def multi_indicator_plot(indicator_country: List[Tuple[str, str]]) -> Any:
    """
    Crea un grafico con gli observables degli indicatori dati e delle nazioni/della nazione dati in input.
    :param indicator_country: Lista di tuple in cui il primo elemento è un id indicator
                              e il secondo la stringa della nazione di 3 caratteri (es. ita)
    :return: il plot da mostrare con .show()
    """
    observable_list = []
    # prendo le serie di osservabili di ciascun indicatore e le salvo in una lista
    for (ind, country) in indicator_country:
        series: List[Observable] = fetch.all_observable_of_indicator(ind, country)
        observable_list.append((ind, country, series))
    return plotter.multi_observables_plot(observable_list)


def retta_reg(ind: str, country: str):
    """Restituisce la retta di regressione di un osservabile per una data nazione"""
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
    serie = fetch.all_observable_of_indicator(ind, country)
    return plotter.diff_prime(serie, True)


def covarianza(ind_country_x: Tuple[str, str], ind_country_y: Tuple[str, str]) -> float:
    """
    Ricava la covarianza degli osservabili di una serie
    :param ind_country_x: id dell'indicatore e stringa della nazione per gli osservabili di cui calcolare la covarianza
    :param ind_country_y: come sopra, possibilmente un indicatore diverso e stessa nazione
    :return: la covarianza degli osservabili
    """
    observables_x: List[Observable] = fetch.all_observable_of_indicator(ind_country_x[0], ind_country_x[1])
    observables_y: List[Observable] = fetch.all_observable_of_indicator(ind_country_y[0], ind_country_y[1])

    serie_x = pd.Series([o.value for o in observables_x if o.value is not None])
    serie_y = pd.Series([o.value for o in observables_y if o.value is not None])

    return serie_x.cov(serie_y)


def cmp_scatter_plot(ind_country_x: Tuple[str, str], ind_country_y: Tuple[str, str]) -> Any:
    """
    Grafica i valori per anno di due diversi indicatori, per visualizzarne la correlazione
    :param ind_country_x: prima coppia di stringhe: id indicatore e nazione (es. usa)
    :param ind_country_y: seconda coppia di stringhe: id indicatore e nazione (es. usa)
    :return: un grafico scatterplot
    """
    observables_x: List[Observable] = fetch.all_observable_of_indicator(ind_country_x[0], ind_country_x[1])
    observables_y: List[Observable] = fetch.all_observable_of_indicator(ind_country_y[0], ind_country_y[1])

    # elimino gli osservabili con valori None
    observables_x = [o for o in observables_x if o.value is not None]
    observables_y = [o for o in observables_y if o.value is not None]

    # Eliminiamo i valori se l'anno dell'osservabile non è presente nell'altra serie di osservabili
    # in questo modo le due serie hanno la stessa dimensione
    list_x: List[Observable] = []
    for i in range(len(observables_x)):
        # se l'anno di x è inclusa negli anni di y, aggiungo l' observable alla lista x
        if observables_x[i].value is not None and observables_x[i].date in [o.date for o in observables_y]:
            list_x.append(observables_x[i])
    list_y: List[Observable] = []
    for i in range(len(observables_y)):
        # se l'anno di y è inclusa negli anni di x, aggiungo l' observable alla lista y
        if observables_y[i].value is not None and observables_y[i].date in [o.date for o in observables_x]:
            list_y.append(observables_y[i])

    return plotter.compare_dataset_scatter(list_x, list_y)
