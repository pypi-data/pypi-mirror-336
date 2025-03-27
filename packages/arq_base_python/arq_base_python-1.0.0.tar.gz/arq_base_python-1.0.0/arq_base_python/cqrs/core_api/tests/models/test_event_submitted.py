import unittest
import pytest
from cqrs.core_api.src.models.event_submitted import (
    EventSubmitted,
)
from cqrs.core_api.src.models.event import Event


class TestEventSubmitted(unittest.TestCase):
    def test_get(self):
        event = Event()
        submitted = EventSubmitted(event)
        self.assertEqual(submitted.get(), event)

    def test_get_validation_status(self):
        submitted = EventSubmitted()
        self.assertEqual(submitted.get_validation_status(), 0)

    def test_set_validation_status(self):
        submitted = EventSubmitted()
        submitted.set_validation_status(1)
        self.assertEqual(submitted.get_validation_status(), 1)

    def test_get_validation_message(self):
        submitted = EventSubmitted()
        self.assertEqual(submitted.get_validation_message(), None)

    def test_set_validation_message(self):
        submitted = EventSubmitted()
        submitted.set_validation_message("Validation message")
        self.assertEqual(submitted.get_validation_message(),
                         "Validation message")

    def test_repr(self):
        event = Event()
        submitted = EventSubmitted(event, 1, "Validation message")
        expected_repr = f"EventSubmitted(evento={event}, validation_status=1, validation_message=Validation message)"
        self.assertEqual(repr(submitted), expected_repr)


# if __name__ == "__main__":
#     unittest.main()
