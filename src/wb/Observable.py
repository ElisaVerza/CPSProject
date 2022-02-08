from .interface import IWbObject


class Observable(IWbObject):
    """
    Classe che racchiude tutte le informazioni ed il valore di un Osservabile
    """

    def __init__(self, indicator_id: int, country_code: str, date: int, value: float):
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
        return self.indicator_id == int(other.indicator_id) and self.country == other.country \
               and int(self.date == other.date) and self.value == float(other.value)

    def to_tuple(self):
        return self.indicator_id, self.country, self.date, self.value
