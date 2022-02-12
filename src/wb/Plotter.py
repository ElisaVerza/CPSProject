from typing import List, Any, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
import pandas as pd

from src.wb.Observable import Observable


class Plotter:

    def multi_observables_plot(self, multiple_observables: List[Tuple[str, str, List[Observable]]]) -> Any:
        """
        Grafica un numero qualsiasi di serie di osservabili nello stesso grafico
        :param multiple_observables: una lista di tuple con id degli indicator, con rispettiva nazione e osservabili.
        :return: il grafico degli osservabili
        """
        ax: plt.axes
        fig: plt.figure
        plt.figure(figsize=(16, 9))
        fig, ax = plt.subplots()
        observable_tuple: Tuple[str, str, List[Observable]]
        line_handles = []
        indic_countries: List[Tuple[str, str]] = []
        for observable_tuple in multiple_observables:
            years: ndarray[int] = np.array([int(obs.date) for obs in observable_tuple[2] if obs.value is not None])
            values: ndarray[int] = np.array([int(obs.value) for obs in observable_tuple[2] if obs.value is not None])
            indic_countries.append((observable_tuple[0], observable_tuple[1]))
            line, = ax.plot(years, values, marker='.')
            line_handles.append(line)

        self.modify_plot(line_handles, ax, indic_countries, "Multiple Observables")
        return plt

    def moving_avg(self, obs: List[Observable], w: int):
        """
        Grafica la media mobile di una serie di osservabili
        :param obs: la lista di osservabili di cui calcolare la media mobile
        :param w: la dimensione della finestra per la media mobile
        :return: il grafico della media mobile
        """
        plt.figure(figsize=(16, 9))
        country = obs[0].country
        ind_id = obs[0].indicator_id

        points = []
        finestra = 0

        val: ndarray[int] = np.array([int(o.value) for o in obs if o.value is not None])
        for i in range(w):
            finestra += val[i]

        for i in range(w, len(val)):
            points.append(finestra / w)
            finestra = finestra + val[i] - val[i - w]
        fig, ax = plt.subplots()
        years: ndarray[int] = np.array([int(o.date) for o in obs if o.value is not None])
        line, = ax.plot(years[:len(points)], points, marker='.')
        self.modify_plot([line], ax, [(ind_id, country)], "Moving Average")

        return plt

    def diff_prime(self, obs: List[Observable], percentage=False):
        """
        Calcola e grafica le differenze prime (anche percentuali) di una serie di osservabili.
        :param obs: la lista di osservabili di cui calcolare la media mobile
        :param percentage: se True, calcola le differenze prime percentuali, altrimenti le differenze prime semplici
        :return: il grafico delle differenze prime [percentuali]
        """
        # uso la dict-comprehension per ricavare un dizionario dalla lista di observable
        series = pd.Series(data={int(o.date): int(o.value) for o in obs if o.value is not None},
                           index=[int(o.date) for o in obs if o.value is not None])
        diff: pd.Series
        title: str

        if not percentage:
            diff = series.diff()
            title = "Prime Difference"
        else:
            diff = series.pct_change()
            title = "Prime Percentage Difference"

        fig, ax = plt.subplots()
        line, = ax.plot(diff)
        self.modify_plot([line], ax, [(obs[0].indicator_id, obs[0].country)], title)
        return plt

    def diff_prime_a_mano(self, obs: List[Observable]):
        """
        Calcola A MANO e grafica le differenze prime di una serie di osservabili
        """
        values = [o.value for o in obs if o.value is not None]
        years = [o.date for o in obs if o.value is not None]

        diff_list = []
        for i in range(1, len(values)):
            diff_list.append(values[i] - values[i - 1])

        fig, ax = plt.subplots()
        line, = ax.plot(np.array(years[1:]), np.array(diff_list))
        self.modify_plot([line], ax, [(obs[0].indicator_id, obs[0].country)],
                         "Prime Differenze housemade")

        return plt

    def diff_prime_percentuali_a_mano(self, obs: List[Observable]):
        """
        Calcola e grafica le differenze prime percentuali di una serie di osservabili
        """
        # uso la dict-comprehension per ricavare un dizionario dalla lista di observable
        values = [o.value for o in obs if o.value is not None]
        years = [o.date for o in obs if o.value is not None]
        diff_list_perc = []
        for i in range(1, len(values)):
            diff_list_perc.append((values[i] - values[i - 1]) / values[i - 1])

        fig, ax = plt.subplots()
        line, = ax.plot(np.array(years[1:]), np.array(diff_list_perc))
        self.modify_plot([line], ax, [(obs[0].indicator_id, obs[0].country)],
                         "Prime Differenze housemade")
        return plt

    def regression_rect(self, obs: List[Observable]):
        """
        Grafica la retta di regressione di una serie di osservabili
        :return: il grafico della retta di regressione
        """
        # Calcolo punti retta regressione
        plt.figure(figsize=(16, 9))
        x_value = np.array([o.date for o in obs if o.value is not None])
        y_value = np.array([int(o.value) for o in obs if o.value is not None])
        x_value = x_value.astype(np.int)
        y_value = y_value.astype(np.int)
        x_mean = x_value.mean()
        y_mean = y_value.mean()

        b1_num = ((x_value - x_mean) * (y_value - y_mean)).sum()
        b1_den = ((x_value - x_mean) ** 2).sum()
        b1 = b1_num / b1_den
        b0 = y_mean - (b1 * x_mean)
        points = [b0 + round(b1, 3) * i for i in x_value]
        fig, ax = plt.subplots()
        regr_line, = ax.plot(x_value, points, marker=None)
        data_line = ax.scatter(x_value, y_value, color="orange", marker='.')
        self.modify_plot([regr_line, data_line], ax,
                         [("Regression Rect", obs[0].country), (obs[0].indicator_id, obs[0].country)],
                         "Regression Rect")
        return plt

    def compare_dataset_scatter(self, obs_x: List[Observable], obs_y: List[Observable]):
        value_x = np.array([o.value for o in obs_x if o.value is not None])
        value_y = np.array([o.value for o in obs_y if o.value is not None])
        fig, ax = plt.subplots()
        data_line = ax.scatter(value_x, value_y, color="orange", marker='.')
        ax.ticklabel_format(style='plain', axis='x')  # nessun tick sull'asse x
        plt.xticks(rotation=20)
        self.modify_plot([data_line], ax,
                         [(obs_x[0].indicator_id, obs_x[0].country), (obs_y[0].indicator_id, obs_y[0].country)],
                         "Scatter Compare Plot")
        return plt

    def modify_plot(self, line_handles: List, ax: plt.axes, indicator_countries_label: List[Tuple[str, str]],
                    title: str):
        rotation = 70
        ax.ticklabel_format(style='plain', axis='y')  # nessun tick sull'asse y


        legend_list = []
        for tup in indicator_countries_label:
            legend_list.append("{} ({})".format(tup[0], tup[1]))

        ax.legend(handles=line_handles, labels=legend_list, loc='upper right')
        plt.yticks(rotation=rotation)
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.grid(linestyle='--', linewidth=0.5)
        plt.title(title, loc='left')
