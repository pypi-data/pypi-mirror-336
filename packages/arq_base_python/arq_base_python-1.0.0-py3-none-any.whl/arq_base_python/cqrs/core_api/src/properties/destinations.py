import abc


class Destinations(abc.ABC):

    @abc.abstractmethod
    def get_publish_destination(self) -> str:
        pass

    @abc.abstractmethod
    def get_suscribre_destination(self) -> str:
        pass
