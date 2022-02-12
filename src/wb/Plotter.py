from typing import List, Dict, Any, Tuple

import matplotlib.pyplot as plt
import numpy as np

from src.wb.Observable import Observable


class Plotter:

    def __init__(self, dict_info: List[Dict]):
        # TODO: Per ora lascialo per retro compatibilità. Poi elimina e usa la lista di observable
        self.info = dict_info

    def observable_plot(self):
        fig, ax = plt.subplots()
        ind: List[str] = []
        c: List[str] = []
        for observable in self.info:
            ind.append(observable["indicator"])
            c.append(observable["country"])
            ax.plot(observable["years"], observable["values"], marker='.', label=observable["country"])
        self.modify_graph(ax, ind, c)
        return plt

    def observables_plot_new(self, multiple_observables: List[Tuple[str, str, List[Observable]]]) -> Any:
        """
        Grafica un numero qualsiasi di serie di osservabili nello stesso grafico

        :param multiple_observables: una lista di tuple con id degli indicator, con rispettiva nazione e osservabili.
        :return: il grafico degli osservabili
        """
        fig, ax = plt.subplots()
        observable_tuple: Tuple[str, str, List[Observable]]
        countries: List[str] = []
        indicators: List[str] = []
        for observable_tuple in multiple_observables:
            years: List[int] = [obs.date for obs in observable_tuple[2]]
            years.reverse()  # TODO: perché vengono scaricati in ordine opposto... Attenzione al DB.
            values: List[float] = [obs.value for obs in observable_tuple[2]]
            values.reverse()
            indicators.insert(0, observable_tuple[0])
            countries.insert(0, observable_tuple[1])
            ax.plot(years, values, marker='.', label=observable_tuple[1])

        self.modify_graph(ax, indicators, countries)
        return plt

    def media_mobile(self, w: int):
        """
        Esegue la media mobile sulle osservabili date
        :param w: la dimensione della finestra per la media mobile
        :return: il grafico delle osservabili a cui è stata applicata la media mobile
        """
        points = []
        finestra = 0
        val = self.info[0]["values"]
        list(map(int, val))
        for i in range(w):
            finestra += val[i]

        for i in range(w, len(val)):
            print(i)
            points.append(finestra / w)
            finestra = finestra + val[i] - val[i - w]
        fig, ax = plt.subplots()
        ax.plot(self.info[0]["years"][:len(points)], points, marker='o')
        self.modify_graph(ax, self.info[0]["indicator"], self.info[0]["country"])

        return plt  # TODO: Restituire l'oggetto grafico

    def media_mobile_new(self, obs: List[Observable], w: int):
        country = obs[0].country
        ind_id = obs[0].indicator_id

        points = []
        finestra = 0
        val: List[int] = [int(o.value) for o in obs]
        # list(map(int, val))
        for i in range(w):
            finestra += val[i]

        for i in range(w, len(val)):
            points.append(finestra / w)
            finestra = finestra + val[i] - val[i - w]
        fig, ax = plt.subplots()
        years = [o.date for o in obs]
        # years.reverse()
        ax.plot(years[:len(points)], points, marker='.')
        self.modify_graph(ax, [ind_id], [country])

        return plt  # TODO: Restituire l'oggetto grafico

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

    def retta_reg(self, obs: List[Observable]):
        """
        Grafica la retta di regressione di una serie di osservabili
        :return: il grafico della retta di regressione
        """
        # Calcolo punti retta regressione
        x_value = np.array(self.info["years"])
        y_value = np.array(self.info["values"])
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
        ax.plot(x_value, points, marker='o')
        ax.scatter(x_value, y_value, color="orange")
        self.modify_graph(ax, self.info["indicator"], self.info["country"])

        return plt

    def modify_graph(self, ax: plt.axes, indicator_label: List[str], country_label: List[str]):
        """
        Modifica il grafico aggiungendoci le diverse Labels.
        :param ax: gli assi del grafico
        :param indicator_label: l'etichetta dell'indicator
        :param country_label: la label per la country
        :return:
        """
        rotation = 70
        ax.ticklabel_format(style='plain', axis='y')
        plt.xticks(rotation=rotation)
        plt.yticks(rotation=rotation)
        plt.xlabel("Date", labelpad=20)
        plt.ylabel("Value", labelpad=20)
        plt.grid(linestyle='--', linewidth=0.5)
        plt.title("Indicator = {}, Country = {}".format(indicator_label, country_label), loc='left', pad=20)


if __name__ == "__main__":
    x = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    y = [3, 765, 123, 87, 234, 23, 234, 677, 987, 19]
    dit = {}
    Plotter([dict]).media_mobile(y, 3)
