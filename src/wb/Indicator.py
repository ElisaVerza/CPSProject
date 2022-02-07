class Indicator:
    """
    Classe che racchiude tutte le informazioni di un Indicatore
    """

    def __init__(self, indicator_id: str, name: str, source_note: str, topic_list: list[int]):
        self.id = indicator_id
        self.name = name
        self.sourceNote = source_note
        self.topic = topic_list

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente il Topic
        """
        # f: permette di formattare la stringa in modo semplice
        return f"Indicator(id={self.id}, name={self.name}, topic={self.topic})"

    def to_tuple(self):
        return self.id, self.name, self.sourceNote, self.topic
