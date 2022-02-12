from typing import List, Tuple

from .interface import IWbObject


class Indicator(IWbObject):
    """
    Classe che racchiude tutte le informazioni di un Indicatore
    """

    def __init__(self, indicator_id: str, name: str, source_note: str, topic_list: List[int]):
        self.indicator_id = indicator_id
        self.name = name
        self.sourceNote = source_note
        self.topics = topic_list

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente il Topic
        """
        # f: permette di formattare la stringa in modo semplice
        return f"Indicator(id={self.indicator_id}, name={self.name}, " \
               f"source_note={self.sourceNote[:10]}... topic={self.topics})"

    def __eq__(self, o) -> bool:
        if len(self.topics) != len(o.topics):
            return False
        for i in range(len(self.topics)):
            if self.topics[i] != int(o.topics[i]):  # TODO: ordine diverso!!!
                return False
        return self.indicator_id == str(o.indicator_id) and self.name == o.name and \
               self.sourceNote == o.sourceNote and self.topics == o.topics

    def to_tuple(self) -> Tuple:
        return self.indicator_id, self.name, self.sourceNote

    def indicator_topic_list(self) -> List[Tuple[str, int]]:
        """
        Metodo di utilità per inserire facilmente i topic dell'indicator nel database.
        :return: restituisce una lista di tuple in cui il primo elemento è sempre l'id dell'indicator,
        mentre il secondo è l'id del topic a cui appartiene l' indicator.
        """
        return [(self.indicator_id, topic) for topic in self.topics]
