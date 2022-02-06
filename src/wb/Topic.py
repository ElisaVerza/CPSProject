class Topic:
    def __init__(self, topic_id: int, value: str, source_note: str):
        self.id = topic_id
        self.value = value
        self.sourceNote = source_note

    def __repr__(self):
        """
        :return: Una stringa che riassume brevemente il Topic
        """
        return f"Topic(id={self.id}, value={self.value})"  # f: permette di formattare la stringa in modo semplice

    def to_tuple(self) -> (int, str, str):
        return self.id, self.value, self.sourceNote
