from Plotter import Plotter
import numpy as np


def three_obs():
    print("Sono qui")

    param_dict = {"indicator": "Nome Indicatore",
                  "country": "Nazione Indicatore",
                  "years": np.asarray([[2001, 2002, 2003, 2004], [2001, 2002, 2003, 2004]]),
                  "values": np.asarray([[1, 2, 3, 4], [7, 8, 5, 4]])
                  }

    obs_plt = Plotter(param_dict)
    obs_plt.observable_plot(2)
    return


if __name__ == "__main__":
    three_obs()
