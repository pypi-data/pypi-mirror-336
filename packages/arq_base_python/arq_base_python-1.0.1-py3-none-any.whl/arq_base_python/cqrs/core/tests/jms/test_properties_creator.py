import unittest
from arq_base_python.cqrs.core.src.properties.developer_mode_props import (
    DeveloperModeProps,
)
from arq_base_python.cqrs.core.src.jms.message_properties import (
    MessageProperties,
)
from arq_base_python.cqrs.core.src.jms.properties_creator import (
    PropertiesCreator,
)


class TestPropertiesCreator(unittest.TestCase):
    def setUp(self):
        developer_node_props = DeveloperModeProps()
        self.properties_creator = PropertiesCreator(developer_node_props)

    def test_for_command(self):
        expected_properties = MessageProperties.create().add("type", "COMMAND")
        actual_properties = self.properties_creator.for_command()
        self.assertEqual(str(expected_properties), str(actual_properties))

    def test_for_event(self):
        scope = "scope"
        app_origen = "appOrigen"
        eventName = "eventName"
        expected_properties = (
            MessageProperties.create()
            .add("type", "EVENT")
            .add("scope", scope)
            .add("appOrigen", app_origen)
            .add("eventName", eventName)
        )
        actual_properties = self.properties_creator.for_event(
            scope, app_origen, eventName
        )
        self.assertEqual(str(expected_properties), str(actual_properties))


# if __name__ == "__main__":
#     unittest.main()
