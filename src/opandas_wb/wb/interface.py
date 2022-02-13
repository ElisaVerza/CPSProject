import abc  # abstract base classes


class IWbObject(abc.ABC):
    """
    Interfaccia per un oggetto di WorldBank (es. Indicator, Observable, Topic)
    """

    @abc.abstractmethod
    def to_tuple(self):
        """
        Metodo per trasformare l'oggetto in una tupla i cui elementi sono
        nello stesso ordine di definizione degli attributi del costruttore
        :return: la tupla con i dati dell'oggetto
        """
        pass
