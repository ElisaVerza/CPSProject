import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from numpy import ndarray
from src.opandas_wb.wb.Observable import Observable
from typing import List, Any, Tuple


def multi_observables_plot(multiple_observables: List[Tuple[str, str, List[Observable]]]) -> Any:
    """
    Grafica un numero qualsiasi di serie di osservabili nello stesso grafico
    :param multiple_observables: una lista di tuple con id degli indicator, con rispettiva nazione e osservabili.
    :return: il grafico degli osservabili
    """
    # ax: plt.axes
    # fig: plt.figure
    # plt.figure(figsize=(16, 9))
    # fig, ax = plt.subplots()
    observable_tuple: Tuple[str, str, List[Observable]]
    line_handles = []
    indic_countries: List[Tuple[str, str]] = []
    # per ogni serie di osservabili, ricavo gli anni e i valori NON NULLI e li aggiungo al grafico
    for observable_tuple in multiple_observables:
        years: ndarray = np.array([int(obs.date) for obs in observable_tuple[2] if obs.value is not None])
        values: ndarray = np.array([obs.value for obs in observable_tuple[2] if obs.value is not None])
        indic_countries.append((observable_tuple[0], observable_tuple[1]))
        # le line handle servono per aggiungere la legenda
        line, = plt.plot(years, values, marker='.')
        line_handles.append(line)

    modify_plot(line_handles, indic_countries, "Multiple Observables")
    return plt


def moving_avg(obs: List[Observable], w: int):
    """
    Grafica la media mobile di una serie di osservabili
    :param obs: la lista di osservabili di cui calcolare la media mobile
    :param w: la dimensione della finestra per la media mobile
    :return: il grafico della media mobile
    """
    # plt.figure(figsize=(16, 9))
    country = obs[0].country
    ind_id = obs[0].indicator_id
    points = []
    finestra = 0

    # ricavo i valori non nulli
    val: ndarray = np.array([o.value for o in obs if o.value is not None])
    for i in range(w):
        finestra += val[i]

    for i in range(w, len(val)):
        points.append(finestra / w)
        finestra = finestra + val[i] - val[i - w]
    # fig, ax = plt.subplots()
    years: ndarray = np.array([int(o.date) for o in obs if o.value is not None])
    line, = plt.plot(years[:len(points)], points, marker='.')
    modify_plot([line], [(ind_id, country)], "Moving Average")

    return plt


def diff_prime(obs: List[Observable], percentage=False):
    """
    Calcola e grafica le differenze prime (anche percentuali) di una serie di osservabili.
    :param obs: la lista di osservabili di cui calcolare la media mobile
    :param percentage: se True, calcola le differenze prime percentuali, altrimenti le differenze prime semplici
    :return: il grafico delle differenze prime [percentuali]
    """
    # uso la dict-comprehension per ricavare un dizionario dalla lista di observable
    series = pd.Series(data={int(o.date): o.value for o in obs if o.value is not None},
                       index=[int(o.date) for o in obs if o.value is not None])
    diff: pd.Series
    title: str

    if not percentage:
        diff = series.diff()
        title = "Prime Difference"
    else:
        diff = series.pct_change()
        title = "Prime Percentage Difference"

    # fig, ax = plt.subplots()
    line, = plt.plot(diff)
    modify_plot([line], [(obs[0].indicator_id, obs[0].country)], title)
    return plt


def diff_prime_a_mano(obs: List[Observable]):
    """
    Calcola A MANO e grafica le differenze prime di una serie di osservabili. Analogo: diff_prime(obs, False)
    """
    values = [o.value for o in obs if o.value is not None]
    years = [o.date for o in obs if o.value is not None]

    diff_list = []
    for i in range(1, len(values)):
        diff_list.append(values[i] - values[i - 1])

    # fig, ax = plt.subplots()
    line, = plt.plot(np.array(years[1:]), np.array(diff_list))
    modify_plot([line], [(obs[0].indicator_id, obs[0].country)], "Prime Differenze housemade")

    return plt


def diff_prime_percentuali_a_mano(obs: List[Observable]):
    """
    Calcola A MANO e grafica le differenze prime percentuali di una serie di osservabili. Analogo: diff_prime(obs, True)
    """
    values = [o.value for o in obs if o.value is not None]
    years = [o.date for o in obs if o.value is not None]
    diff_list_perc = []
    for i in range(1, len(values)):
        diff_list_perc.append((values[i] - values[i - 1]) / values[i - 1])

    # fig, ax = plt.subplots()
    line, = plt.plot(np.array(years[1:]), np.array(diff_list_perc))
    modify_plot([line], [(obs[0].indicator_id, obs[0].country)], "Prime Percentage Difference housemade")
    return plt


def regression_rect(obs: List[Observable]):
    """
    Grafica la retta di regressione di una serie di osservabili
    :return: il grafico della retta di regressione
    """
    # Calcolo punti retta regressione
    x_value = np.array([o.date for o in obs if o.value is not None])
    y_value = np.array([o.value for o in obs if o.value is not None])
    x_value = x_value.astype(np.int)
    y_value = y_value.astype(np.int)
    x_mean = x_value.mean()
    y_mean = y_value.mean()

    b1_num = ((x_value - x_mean) * (y_value - y_mean)).sum()
    b1_den = ((x_value - x_mean) ** 2).sum()
    b1 = b1_num / b1_den
    b0 = y_mean - (b1 * x_mean)
    points = [b0 + round(b1, 3) * i for i in x_value]
    # fig, ax = plt.subplots()
    regr_line, = plt.plot(x_value, points, marker=None)
    data_line = plt.scatter(x_value, y_value, color="orange", marker='.')
    modify_plot([regr_line, data_line], [("Regression Rect", obs[0].country), (obs[0].indicator_id, obs[0].country)],
                "Regression Rect")
    return plt


def compare_dataset_scatter(obs_x: List[Observable], obs_y: List[Observable]):
    """
    Crea il grafico che contiene i valori per anno dei due osservabili worldbank
    :param obs_x: gli osservabili del primo indicatore
    :param obs_y: gli osservabili del secondo indicatore.
    :return: il grafico scatterplot che confronta le due serie degli indicatori
    """
    value_x = np.array([o.value for o in obs_x if o.value is not None])
    value_y = np.array([o.value for o in obs_y if o.value is not None])
    # fig, ax = plt.subplots()
    data_line = plt.scatter(value_x, value_y, color="orange", marker='.')
    plt.ticklabel_format(style='plain', axis='x')  # nessun tick sull'asse x
    plt.xticks(rotation=20)

    plt.ticklabel_format(style='plain', axis='y')  # nessun tick sull'asse y e rimuove la notazione scientifica
    # modifico la rotazione sull' asse y
    plt.yticks(rotation=70)
    # Etichette e stili
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title("Scatter Compare Plot", loc='left')
    plt.xlabel(obs_x[0].indicator_id)
    plt.ylabel(obs_y[0].indicator_id)

    return plt


def modify_plot(line_handles: List, indicator_countries_label: List[Tuple[str, str]], title: str):
    """
    Funzione di utilità che abbellisce i grafici
    :param line_handles: lista di handle delle serie, spesso la lista ha un solo elemento.
    :param indicator_countries_label: lista di tuple (id indicatore, nazione), una per ogni indicatore da graficare
    :param title: titolo del grafico
    """
    plt.ticklabel_format(style='plain', axis='y')  # nessun tick sull'asse y e rimuove la notazione scientifica

    # crea la lista di stringhe da visualizzare nella legenda
    legend_list = []
    for tup in indicator_countries_label:
        legend_list.append("{} ({})".format(tup[0], tup[1]))

    # aggiunge una legenda al grafico in alto a destra
    plt.legend(handles=line_handles, labels=legend_list, loc='upper right')

    # modifico la rotazione sull' asse y
    plt.yticks(rotation=70)

    # Etichette e stili
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(linestyle='--', linewidth=0.5)
    plt.title(title, loc='left')
