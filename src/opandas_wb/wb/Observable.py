from typing import Optional

from .interface import IWbObject


class Observable(IWbObject):
    """
    Classe che racchiude tutte le informazioni ed il valore di un Osservabile
    """

    def __init__(self, indicator_id: str, country_code: str, date: int, value: Optional[float]):
        self.indicator_id = indicator_id
        self.country = country_code
        self.date = date
        self.value = value

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente l'Osservabile
        """
        # f: permette di formattare la stringa in modo semplice
        return f"Observable(indicator_id={self.indicator_id}, country={self.country}, " \
               f"date={self.date}, value={self.value})"

    def __eq__(self, other):
        return self.indicator_id == str(other.indicator_id) and self.country == other.country \
               and self.date == int(other.date) and ((self.value == other.value) or (self.value is None and other.value is None))

    def to_tuple(self):
        return self.indicator_id, self.country, self.date, self.value
