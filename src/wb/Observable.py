class Observable:
    """
    Classe che racchiude tutte le informazioni ed il valore di un Osservabile
    """
    def __init__(self, indicator_id: str, country_code: str, date: int, value: float):
        self.id = indicator_id
        self.country = country_code
        self.date = date
        self.value = value

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente l'Osservabile
        """
        # f: permette di formattare la stringa in modo semplice
        return f"Indicator(indicator_id={self.id}, country={self.country}, date={self.date}, value={self.value})"

    def to_tuple(self):
        return self.id, self.country, self.date, self.value
