from typing import List

from src.wb.Observable import Observable

from src.wb.Plotter import Plotter
import src.wb.download_wb as dl
import numpy as np


def test_three_obs(ind: List[str], country: List[str]):
    # TODO: Istruzione cerca osservabili su db
    param_dict = []
    for i in range(len(ind)):
        all_values = dl.download_observables_of_indicator(ind[i], country[i])
        param_dict.append({"indicator": all_values[0].indicator_id,
                           "country": all_values[0].country,
                           "years": [],
                           "values": []
                           })
        for obs in all_values:
            if obs.value is None:
                obs.value = 0

            param_dict[i].get("years").insert(0, obs.date)
            param_dict[i].get("values").insert(0, obs.value)
            print(param_dict[i])

    obs_plt = Plotter(param_dict)
    obs_plt.observable_plot().show()

    return


if __name__ == "__main__":
    test_three_obs(ind=['AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO'], country=['usa', 'HPC', 'LIE'])
