from typing import List
from src.wb.Plotter import Plotter
import src.wb.download_wb as dl


def three_obs(ind: List[str], country: List[str]):
    """Restituisce il grafico di un osservabile"""
    param_dict = []
    for i in range(len(ind)):
        all_values = dl.download_observables_of_indicator(ind[i], country[i])
        # todo usare fetch.all_observable_of_indicator
        param_dict.append({"indicator": all_values[0].indicator_id,
                           "country": all_values[0].country,
                           "years": [],
                           "values": []
                           })
        for obs in all_values:
            param_dict[i].get("years").insert(0, obs.date)
            param_dict[i].get("values").insert(0, obs.value if obs.value is not None else 0)
            # TODO: METTERE NELLA RELAZIONE
    plotter = Plotter(param_dict)
    return plotter.observable_plot()


def retta_reg(ind: str, country: str):
    """Restituisce la retta di regressione di un osservabile per una data nazione"""
    values = dl.download_observables_of_indicator(ind, country)  # todo usare fetch.all_observable_of_indicator
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    plotter = Plotter(param_dict)
    return plotter.retta_reg()


def media_mobile(ind: str, country: str, win: int):
    """Istruzione cerca osservabili su db"""
    values = dl.download_observables_of_indicator(ind, country)  # todo usare fetch.all_observable_of_indicator
    param_dict = {"indicator": values[0].indicator_id,
                  "country": values[0].country,
                  "years": [],
                  "values": []
                  }
    for obs in values:
        param_dict.get("years").insert(0, obs.date)
        param_dict.get("values").insert(0, obs.value if obs.value is not None else 0)
    plotter = Plotter(param_dict)
    return plotter.media_mobile(win)
