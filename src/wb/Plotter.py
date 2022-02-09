# import matplotlib as mpl
# import matplotlib.pyplot
from typing import List

import matplotlib.pyplot as plt


# import numpy as np

class Plotter:
    def __init__(self, dict_info):
        self.info = dict_info

    def observable_plot(self):
        """
        Grafica un numero qualsiasi di osservabili
        :return: il grafico degli osservabili
        """
        rotation = 70
        fig, ax = plt.subplots()
        ind: List[str] = []
        c: List[str] = []
        for i in self.info:
            ind.append(i["indicator"])
            c.append(i["country"])
            ax.plot(i["years"], i["values"], marker='o', label=i["country"])
        ax.ticklabel_format(style='plain', axis='y')
        plt.legend(loc="upper left")
        plt.xticks(rotation=rotation)
        plt.yticks(rotation=rotation)
        plt.xlabel("Date", labelpad=20)
        plt.ylabel("Value", labelpad=20)
        plt.grid(linestyle='--', linewidth=0.5)
        plt.title("Indicator = {}, Country = {}".format(ind, c), loc='left', pad=20)

        return plt

    def media_mobile(self):
        # TODO: metodo per calcolare e graficare media mobile
        return

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
        # TODO: metodo per calcolare e graficare differenze prime percentuali
        return


"""
if __name__ == "__main__":
    param_dict = {
        "years": [2001, 2002, 2003, 2004],
        "values": [1, 2, 3, 4],
        "indicator": "Nome Indicatore",
        "country": "Nazione Indicatore"
    }
    Plotter().observable_plot(param_dict)
"""
