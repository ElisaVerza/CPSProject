from .interface import IWbObject


class Topic(IWbObject):
    """
    Classe che racchiude tutte le informazioni di un Topic di WorldBank
    """

    def __init__(self, topic_id: int, value: str, source_note: str):
        self.topic_id = topic_id
        self.value = value
        self.sourceNote = source_note

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente il Topic
        """
        return f"Topic(id={self.topic_id}, value={self.value}, sourceNote={self.sourceNote[:10]}...)"

    def __eq__(self, o) -> bool:
        # Importante: poiché o è di tipo object, trasforma TUTTO in stringa. I parametri vanno convertiti manualmente
        return self.topic_id == int(o.topic_id) and self.value == o.value and self.sourceNote == o.sourceNote

    def to_tuple(self) -> (int, str, str):
        return self.topic_id, self.value, self.sourceNote
