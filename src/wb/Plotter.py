from typing import List, Any, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray

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

        self.modify_graph(line_handles, ax, indic_countries, "Multiple Observables")
        return plt

    def moving_avg(self, obs: List[Observable], w: int):
        """
        Grafica la media mobile di una serie di osservabili
        :param obs:
        :param w:
        :return:
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
        self.modify_graph([line], ax, [(ind_id, country)], "Moving Average")

        return plt

    def diff_prime(self, obs: List[Observable]):
        # TODO: metodo per calcolare e graficare differenze prime
        return

    def diff_prime_p(self, obs: List[Observable]):
        # TODO: metodo per calcolare e graficare differenze prime percentuali
        return

    def covarianza(self, obs: List[Observable]) -> float:
        media_campionaria = None
        # covar = 1/n Sum(k=1^n) (x_k, media_campionaria)^2
        # TODO: metodo per calcolare e graficare covarianza
        return 0.0

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
        self.modify_graph([regr_line, data_line], ax,
                          [("Regression Rect", obs[0].country), (obs[0].indicator_id, obs[0].country)],
                          "Regression Rect")

        return plt

    def modify_graph(self, line_handles: List, ax: plt.axes, indicator_countries_label: List[Tuple[str, str]],
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
