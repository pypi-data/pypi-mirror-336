from cqrs.core_api.src.properties.destinations import (
    Destinations,
)


class MQDestinations(Destinations):

    def __init__(
        self,
        publish_destination: str,
        suscribre_destination: str,
        ui_destination: str,
    ) -> None:
        self.publish_destination = publish_destination
        self.suscribre_destination = suscribre_destination
        self.ui_destination = ui_destination

    def get_publish_destination(self) -> str:
        return self.publish_destination

    def get_suscribre_destination(self) -> str:
        return self.suscribre_destination

    def get_ui_destination(self) -> str:
        return self.ui_destination

    def __repr__(self) -> str:
        return f"MQDestinations(publishDestination={self.publish_destination}, suscribreDestination={self.suscribre_destination}, uiDestination={self.ui_destination})"
