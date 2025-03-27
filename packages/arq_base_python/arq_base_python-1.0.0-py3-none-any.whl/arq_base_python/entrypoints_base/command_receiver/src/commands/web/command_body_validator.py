import re
import json
import logging
from dataclasses import fields

from reactivex import Observable, of, operators as op

from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)
from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.handler_registry import (
    HandlerRegistry,
)
from entrypoints_base.command_receiver.src.commands.invalid_regex import (
    InvalidRegex,
)


class CommandBodyValidator:
    def __init__(
        self,
        handler_registry: HandlerRegistry,
        invalid_regex: InvalidRegex,
    ):
        self.handler_registry = handler_registry
        self.invalid_regex = invalid_regex
        self.REGEX_DEFAULT = r"[~!@#&|;\'?/*$^+\\\\<>]"
        self.log = logging.getLogger(__name__)

    def receive_validate_contract_observer(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self._valid_contract),
            # op.catch(of(CommandSubmitted()))
        )
        return observer_object

    def call_validate_command_name(self, command: CommandSubmitted):
        return self._validate_command_name(
            command=command, handler_registry=self.handler_registry
        )

    def receive_validate_command_name_observer(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.call_validate_command_name),
            # op.catch(of(CommandSubmitted()))
        )
        return observer_object

    def receive_validate_special_characters_observer(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self._validate_command_special_characters),
            # op.catch(of(CommandSubmitted()))
        )
        return observer_object

    def perform_validation(self, command: CommandSubmitted) -> Observable[CommandSubmitted]:
        validate_contract_observer = self.receive_validate_contract_observer(
            observer_object=command
        )

        validate_command_name_observer = self.receive_validate_command_name_observer(
            observer_object=validate_contract_observer
        )

        validate_special_characters_observer = (
            self.receive_validate_special_characters_observer(
                observer_object=validate_command_name_observer
            )
        )

        return validate_special_characters_observer

    @staticmethod
    def _is_command_name_empty(command: CommandSubmitted) -> bool:
        if command is None:
            return True
        else:
            if (
                (command.get() is None)
                or (command.get().nombre is None)
                or (command.get().nombre == "")
            ):
                return True
        return False

    def _valid_contract(self, command: CommandSubmitted) -> CommandSubmitted:
        self.log.debug("Commando a Validar: %s", command)
        if self._is_command_name_empty(command):
            command.set_validation_status(400)
            command.set_validation_message("Nombre del comando es obligatorio")
        return command

    def _command_declared_in_handler_registry(
        self, command: CommandSubmitted, handler_registry: HandlerRegistry
    ) -> bool:
        return any(
            command.get().nombre == elemento.get_message_name()
            for elemento in handler_registry.get_command_handlers()
        )

    def _validate_command_name(
        self, command: CommandSubmitted, handler_registry: HandlerRegistry
    ) -> CommandSubmitted:
        self.log.debug("Commando a Validar: %s", command)
        if command.get_validation_status() != 0:
            return command
        if not self._command_declared_in_handler_registry(command, handler_registry):
            command.set_validation_status(400)
            command.set_validation_message("Nombre del comando no registrado")
        return command

    def _validate_command_special_characters(
        self,
        command: CommandSubmitted,
    ) -> CommandSubmitted:
        self.log.debug(
            "Validando caracteres especiales en los campos del comando")
        # TODO: Esta validacion debe ir despues de hacer debug de actual_fields (se requiere corregir reactividad)
        if command.get_validation_status() != 0:
            return command
        actual_fields = self._get_filtered_field_names(command.get())
        self.log.debug("Actual field names: %s", actual_fields)
        fields_with_special_characters = {}
        for field in actual_fields:
            try:
                field_value = getattr(command.get(), field) if field is not "payload" else json.dumps(
                    getattr(command.get(), field), ensure_ascii=False)
                field_regex = self.invalid_regex.get_regex(field)
                if field_value == None:
                    continue
                self.log.debug(f"value: {field_value}")
                if re.search(field_regex, str(field_value)):
                    # print(
                    #     f"Caracteres especiales encontrados en el campo {field}: {field_value} | {field_regex}"
                    # )
                    fields_with_special_characters[field] = field_regex
            except TypeError:
                pass

        self.log.debug(
            "validation_status: %s - %s",
            command.get_validation_status(),
            command.get_validation_message(),
        )
        self.log.debug("-" * 50)
        if fields_with_special_characters:
            command.set_validation_status(400)
            command.set_validation_message(
                f"Contiene caracteres no permitidos: {fields_with_special_characters}"
            )
        return command

    def _get_filtered_field_names(self, cls):
        return list(
            filter(
                lambda x: x is not None,
                map(
                    lambda x: None if x.name.startswith("_") else x.name,
                    fields(cls),
                ),
            )
        )
