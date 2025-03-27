import logging
import json
from collections import deque

from reactivex import of, operators as op

from cqrs.core_api.src.event.event_error import EventError
from cqrs.core_api.src.fallback.storage_fallback import StorageFallback


class FileQueueFallBack(StorageFallback):

    log = logging.getLogger(__name__)

    def __init__(self, persistentFsQueue: deque):
        self.persistentFsQueue = persistentFsQueue

    def add(self, var1: EventError):
        try:
            event_error = of(var1)
        except Exception as e:
            self.log.error(f"Se genero un error: {str(e)}")
            event_error = of(EventError())

        json_event_error = self.receive_event_error(
            event_error_observable=event_error
        )

        stored_fallback = self.receive_json_event_error(
            json_event_error_observable=of(json_event_error)
        )

        return stored_fallback

    def receive_event_error(self, event_error_observable):
        observer_object = event_error_observable.pipe(
            op.map(self.__build_json)
        )
        return observer_object.run()

    @staticmethod
    def __build_json(event_error_observable):
        return json.dumps(event_error_observable.__dict__)

    def receive_json_event_error(self, json_event_error_observable):
        observer_object = json_event_error_observable.pipe(
            op.map(self.__store_json)
        )
        return observer_object.run()

    def __store_json(self, json_event_error_observable):
        try:
            self.persistentFsQueue.append(json_event_error_observable)
            return True
        except Exception as var3:
            self.log.error(
                f"Error almacenando en mecanismo de fallback en filesystem, {str(var3)}")
            return False
