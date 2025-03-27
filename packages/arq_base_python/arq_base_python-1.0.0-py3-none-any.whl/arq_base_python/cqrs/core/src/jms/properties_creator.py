from cqrs.core.src.properties.developer_mode_props import (
    DeveloperModeProps,
)
from cqrs.core.src.jms.message_properties import (
    MessageProperties,
)


class PropertiesCreator:
    def __init__(self, developer_node_props: DeveloperModeProps):
        self.developer_node_props = developer_node_props

    def for_command(self) -> MessageProperties:
        return self._for_message("COMMAND", None, None, None)

    def for_event(
        self, scope: str, app_origen: str, eventName: str
    ) -> MessageProperties:
        return self._for_message("EVENT", scope, app_origen, eventName)

    def _for_message(
        self, type: str, scope: str | None, app_origen: str | None, eventName: str | None
    ) -> MessageProperties:
        var10000 = (
            MessageProperties.create()
            .add("type", type)
            .add("scope", scope)
            .add("appOrigen", app_origen)
            .add("eventName", eventName)
        )
        var10001 = self.developer_node_props.is_developer_mode()
        var10003 = self.developer_node_props
        return var10000.add_if(var10001, "dev", var10003.get_devid)
