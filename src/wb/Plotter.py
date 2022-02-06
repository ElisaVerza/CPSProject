# import matplotlib as mpl
# import matplotlib.pyplot
import matplotlib.pyplot as plt


import numpy as np

class Plotter:
    def __init__(self, dict_info):
        self.info = dict_info

    def observable_plot(self, plt_num):
        fig, ax = plt.subplots()
        for i in range(plt_num):
            ax.plot(self.info["years"][i], self.info["values"][i], marker='o')
        plt.show()
        #TODO: Come vanno salvati i plot?
        return

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