import unittest
from unittest.mock import MagicMock
from cqrs.core.src.jms.message_publisher import MessagePublisher
from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)
from cqrs.core_api.src.jms.core_message_publisher import (
    CoreMessagePublisher,
)


class TestMessagePublisher(unittest.TestCase):

    def setUp(self):
        self.mock_core_message_publisher = MagicMock(spec=CoreMessagePublisher)
        self.message_publisher = MessagePublisher(
            self.mock_core_message_publisher)

    def test_publish_with_submittable_has_content(self):
        submittable = CommandSubmitted()
        self.mock_core_message_publisher.publish.return_value = None

        self.message_publisher.publish(submittable)

        self.mock_core_message_publisher.publish()

        # c = self.mock_core_message_publisher.publish.assert_called_once_with(submittable.get())

    def test_publish_with_submittable_has_no_content(self):
        submittable = MagicMock(spec=CommandSubmitted)
        submittable.get.return_value = None
        self.mock_core_message_publisher.publish.return_value = None

        self.message_publisher.publish(submittable)

        self.mock_core_message_publisher.publish.assert_not_called()
        # self.message_publisher.log.error.assert_called_once_with(
        #     "No se puede publicar un comando o evento nulo"
        # )

    # def test_initialize_event_properties(self):
    #     event = MagicMock()
    #     submittable = MagicMock()
    #     self.message_publisher.publish_for_log = MagicMock(return_value="log_message")

    #     result = self.message_publisher.initialize_event_properties(event, submittable)

    #     self.assertEqual(result, "log_message")
    #     self.message_publisher.publish_for_log.assert_called_once_with(submittable)


# if __name__ == "__main__":
#     unittest.main()
