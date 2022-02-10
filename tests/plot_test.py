from typing import List
from src.wb.Plotter import Plotter
import src.wb.download_wb as dl


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
            param_dict[i].get("years").insert(0, obs.date)
            param_dict[i].get("values").insert(0, obs.value if obs.value is not None else 0)
    obs_plt = Plotter(param_dict)
    obs_plt.observable_plot().show()

    return


def test_retta_reg(ind: str, country: str):
    # TODO: Istruzione cerca osservabili su db
    values = dl.download_observables_of_indicator(ind, country)
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    reg = Plotter(param_dict)
    reg.retta_reg().show()

    return


def test_media_mobile(ind: str, country: str, win: int):
    # TODO: Istruzione cerca osservabili su db
    values = dl.download_observables_of_indicator(ind, country)
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    mean = Plotter(param_dict)
    mean.media_mobile(win).show()

    return


if __name__ == "__main__":
    test_media_mobile(ind='AG.AGR.TRAC.NO', country='usa', win=3)
