# import matplotlib as mpl
# import matplotlib.pyplot
from typing import List

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, dict_info):
        self.info = dict_info

    def observable_plot(self):
        """
        Grafica un numero qualsiasi di osservabili
        :return: il grafico degli osservabili
        """
        fig, ax = plt.subplots()
        ind: List[str] = []
        c: List[str] = []
        for i in self.info:
            ind.append(i["indicator"])
            c.append(i["country"])
            ax.plot(i["years"], i["values"], marker='o', label=i["country"])
        self.make_graph(ax, ind, c)

        return plt

    def media_mobile(self, w):
        points = []
        finestra = 0
        val = self.info["values"]
        list(map(int, val))
        for i in range(w):
            finestra += val[i]

        for i in range(w, len(val)):
            print(i)
            points.append(finestra / w)
            finestra = finestra + val[i] - val[i - w]
        fig, ax = plt.subplots()
        ax.plot(self.info["years"][:len(points)], points, marker='o')
        self.make_graph(ax, self.info["indicator"], self.info["country"])

        return plt

    def diff_prime(self):
        # TODO: metodo per calcolare e graficare differenze prime
        return

    def diff_prime_p(self):
        # TODO: metodo per calcolare e graficare differenze prime percentuali
        return

    def covarianza(self):
        # TODO: metodo per calcolare e graficare differenze prime percentuali
        return

    def retta_reg(self):
        """
        Grafica la retta di regressione di un osservabile
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
        self.make_graph(ax, self.info["indicator"], self.info["country"])

        return plt

    def make_graph(self, ax: plt.axes, ind_label, c_label):
        rotation = 70
        ax.ticklabel_format(style='plain', axis='y')
        plt.xticks(rotation=rotation)
        plt.yticks(rotation=rotation)
        plt.xlabel("Date", labelpad=20)
        plt.ylabel("Value", labelpad=20)
        plt.grid(linestyle='--', linewidth=0.5)
        plt.title("Indicator = {}, Country = {}".format(ind_label, c_label), loc='left', pad=20)
        return


if __name__ == "__main__":
    x = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
    y = [3, 765, 123, 87, 234, 23, 234, 677, 987, 19]
    dit = {}
    Plotter(dict).media_mobile(y, 3)
