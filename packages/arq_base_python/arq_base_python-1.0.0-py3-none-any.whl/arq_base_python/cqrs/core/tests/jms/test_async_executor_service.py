from reactivex import Observable
import reactivex
from cqrs.core_api.src.event.event_result import EventResult
from cqrs.core_api.src.models.event import Event
from cqrs.core_api.src.models.command_submitted import CommandSubmitted
from cqrs.core_api.src.models.command import Command
from unittest.mock import Mock, MagicMock
import uuid
import json

import pytest
from faker import Faker

from cqrs.core.src.jms.async_executor_service import AsyncExecutorService
from cqrs.core.src.jms.tipo_ejecutable import TipoEjecutable
from cqrs.core.src.model.exec_dto import ExecDTO
from cqrs.core_api.src.messaging.message_serializer import MessageSerializer
from cqrs.core_api.src.models.event_submitted import EventSubmitted
from cqrs.core_api.src.models.received_message import ReceivedMessage
from jano.core.src.secured_application import SecuredApplication
from cqrs.core.src.jms.send_message_to_mq import SendMessageToMQ
from cqrs.core.src.properties.developer_mode_props import DeveloperModeProps
from cqrs.core.src.jms.properties_creator import PropertiesCreator
from cqrs.core_api.src.properties.destinations import Destinations
from cqrs.core_api.src.jms.concrete_sender import ConcreteSender
from cqrs.core.src.handlers.handler_resolver import HandlerResolver


fake = Faker()


@pytest.fixture()
def setup_serializer():
    return MagicMock(spec=MessageSerializer)


@pytest.fixture()
def setup_developer_mode_props():
    return DeveloperModeProps()


@pytest.fixture()
def setup_properties_creator(setup_developer_mode_props):
    return PropertiesCreator(
        developer_node_props=setup_developer_mode_props
    )


@pytest.fixture()
def setup_mq_destinations():
    return MagicMock(spec=Destinations)


@pytest.fixture()
def setup_sender():
    return MagicMock(spec=ConcreteSender)


@pytest.fixture()
def setup_send_message_to_mq(setup_properties_creator, setup_mq_destinations, setup_serializer, setup_sender):
    return SendMessageToMQ(
        properties_creator=setup_properties_creator,
        mq_destinations=setup_mq_destinations,
        serializer=setup_serializer,
        sender=setup_sender
    )


@pytest.fixture()
def setup_secured_application():
    return MagicMock(spec=SecuredApplication)


@pytest.fixture()
def setup_handler_resolver():
    return MagicMock(spec=HandlerResolver)


@pytest.fixture()
def setup_async_executor_service(setup_serializer, setup_secured_application, setup_send_message_to_mq, setup_handler_resolver):
    # Configuring the secured application mock
    setup_secured_application.id_app_proteccion = 123
    setup_secured_application.name = "Test App"

    async_executor_service = AsyncExecutorService(
        serializer=setup_serializer,
        secured_application=setup_secured_application,
        send_message_to_mq=setup_send_message_to_mq,
        handler_resolver=setup_handler_resolver
    )

    return async_executor_service


@pytest.fixture()
def setup_receive_message():
    return ReceivedMessage(
        # type= "TYPE-DESCONOCIDO",
        type="COMMAND",
        # "type": "EVENT",
        # "type": "LOG",
        content=json.dumps({"one": "two"}),
        jmsID=str(uuid.uuid4())
    )


@pytest.fixture()
def setup_tipo_ejecutable():
    return TipoEjecutable.COMANDO


def test_execute(setup_async_executor_service, setup_receive_message, setup_tipo_ejecutable):
    assert setup_async_executor_service.execute(
        tipo=setup_tipo_ejecutable, body=setup_receive_message)


def test_convertir_dto(setup_async_executor_service, setup_receive_message, setup_tipo_ejecutable):
    assert isinstance(
        setup_async_executor_service.convertir_a_dto(
            tipo=setup_tipo_ejecutable, cuerpo=setup_receive_message),
        ExecDTO
    )


@pytest.fixture
def setup_common_body():
    command = Command(usuario={"ip": "SomeIP"}, dni={
                      "tipoIdentificacion": "CC", "identificacion": "SomeDNI"})
    command.id = "SomeCommandId"
    return command


@pytest.fixture
def setup_submitted(setup_common_body):
    command_submitted = Mock(spec=CommandSubmitted)
    command_submitted.get.return_value = setup_common_body
    return command_submitted


@pytest.fixture
def setup_exec_dto(setup_submitted):
    exec_dto = ExecDTO(tipo=TipoEjecutable.COMANDO,
                       submitted=setup_submitted)
    return exec_dto


@pytest.fixture
def setup_event():
    event = Event()
    event.id = None
    event.idComando = None
    event.usuario = None
    event.dni = None
    return event


def test_decorar_resultado(setup_async_executor_service, setup_exec_dto, setup_event):
    # Arrange
    async_executor_service = setup_async_executor_service
    exec_dto = setup_exec_dto
    event = setup_event

    # Act
    result = async_executor_service._AsyncExecutorService__decorar_resultado(
        exec_dto, event)

    # Assert
    assert result.get().id is not None
    assert result.get().aplicacion_origen.id_aplicacion_origen == "123"
    assert result.get().aplicacion_origen.nombre_aplicacion_origen == "Test App"
    assert result.get().aplicacion_emisora.id_aplicacion_emisora == "123"
    assert result.get().aplicacion_emisora.nombre_aplicacion_emisora == "Test App"
    assert result.get().idComando == "SomeCommandId"
    assert result.get().timestamp is not None
    assert result.get().resultado == EventResult.EXITO.name
    assert result.get().usuario.ip == "SomeIP"
    assert result.get().dni.identificacion == "SomeDNI"


def test_execute_with_valid_body(setup_async_executor_service, setup_tipo_ejecutable):
    body = '{"key": "value"}'
    result = setup_async_executor_service.execute(
        tipo=setup_tipo_ejecutable, body=body)
    assert isinstance(result, Observable)


def test_execute_with_invalid_body(setup_async_executor_service, setup_tipo_ejecutable, setup_serializer):
    setup_serializer.to_command_submitted.side_effect = Exception
    body = 'invalid json'
    with pytest.raises(Exception):
        setup_async_executor_service.execute(
            tipo=setup_tipo_ejecutable, body=body).subscribe()


def test_convertir_a_dto_command(setup_async_executor_service, setup_tipo_ejecutable):
    body = '{"key": "value"}'
    dto = setup_async_executor_service.convertir_a_dto(
        tipo=setup_tipo_ejecutable, cuerpo=body)
    assert isinstance(dto, ExecDTO)
    assert dto.tipo == setup_tipo_ejecutable


def test_convertir_a_dto_event(setup_async_executor_service):
    body = '{"key": "value"}'
    dto = setup_async_executor_service.convertir_a_dto(
        tipo=TipoEjecutable.EVENTO, cuerpo=body)
    assert isinstance(dto, ExecDTO)
    assert dto.tipo == TipoEjecutable.EVENTO


def test_check_for_no_ui_event(setup_async_executor_service, setup_exec_dto):
    result = setup_async_executor_service._AsyncExecutorService__check_for_no_ui_event(
        setup_exec_dto)
    assert result is True


def test_find_handler(setup_async_executor_service, setup_exec_dto):
    handler = setup_async_executor_service._AsyncExecutorService__find_handler(
        setup_exec_dto)
    assert handler is not None


@pytest.mark.asyncio
async def test_publicar_eventos(setup_async_executor_service, setup_exec_dto, setup_event):
    event_observable = reactivex.just(setup_event)
    result = setup_async_executor_service._AsyncExecutorService__publicar_eventos(
        event_observable, setup_exec_dto)
    assert isinstance(result, Observable)
    items = []
    result.subscribe(on_next=lambda x: items.append(x))
    assert len(items) > 0


@pytest.mark.asyncio
async def test_publicar_evento(setup_async_executor_service, setup_event):
    event_submitted = EventSubmitted(setup_event)
    result = setup_async_executor_service._AsyncExecutorService__publicar_evento(
        event_submitted)
    assert isinstance(result, Observable)
    items = []
    result.subscribe(on_next=lambda x: items.append(x))
    assert len(items) > 0


def test_decorar_resultado(setup_async_executor_service, setup_exec_dto, setup_event):
    result = setup_async_executor_service._AsyncExecutorService__decorar_resultado(
        setup_exec_dto, setup_event)
    assert isinstance(result, EventSubmitted)
    assert result.get().id is not None


def test_execute_with_handler(setup_async_executor_service, setup_exec_dto):
    handler = MagicMock()
    handler.get_handler.return_value = lambda x: reactivex.just(x)
    handler.get_input_class.return_value = dict
    result = setup_async_executor_service.execute_with_handler(
        setup_exec_dto, handler)
    assert isinstance(result, Observable)
    items = []
    result.subscribe(on_next=lambda x: items.append(x))
    assert len(items) > 0


def test_flat_map_with_handler(setup_async_executor_service, setup_exec_dto, setup_event):
    # Arrange
    handler = MagicMock()
    handler.get_handler.return_value = lambda x: reactivex.just(x)
    handler.get_input_class.return_value = dict
    setup_async_executor_service._AsyncExecutorService__find_handler = MagicMock(
        return_value=handler)
    setup_async_executor_service.execute_with_handler = MagicMock(
        return_value=reactivex.just(setup_event))
    setup_async_executor_service._AsyncExecutorService__publicar_eventos = MagicMock(
        return_value=reactivex.just(setup_event))

    # Act
    result = setup_async_executor_service._AsyncExecutorService__flat_map(
        setup_exec_dto)

    # Assert
    assert isinstance(result, Observable)
    items = []
    result.subscribe(on_next=lambda x: items.append(x))
    assert len(items) > 0
    setup_async_executor_service._AsyncExecutorService__find_handler.assert_called_once_with(
        exec_dto=setup_exec_dto)
    setup_async_executor_service.execute_with_handler.assert_called_once_with(
        setup_exec_dto, handler)
    setup_async_executor_service._AsyncExecutorService__publicar_eventos.assert_called_once()


def test_flat_map_without_handler(setup_async_executor_service, setup_exec_dto):
    # Arrange
    setup_async_executor_service._AsyncExecutorService__find_handler = MagicMock(
        return_value=None)
    setup_async_executor_service.log.error = MagicMock()

    # Act
    result = setup_async_executor_service._AsyncExecutorService__flat_map(
        setup_exec_dto)

    # Assert
    assert isinstance(result, Observable)
    items = []
    result.subscribe(on_next=lambda x: items.append(x))
    assert len(items) == 0
    setup_async_executor_service._AsyncExecutorService__find_handler.assert_called_once_with(
        exec_dto=setup_exec_dto)
    setup_async_executor_service.log.error.assert_called_once_with(
        f"No se encontro un handler para el evento {setup_exec_dto.submitted.get().nombre}"
    )


def test_flat_map_with_handler_exception(setup_async_executor_service, setup_exec_dto):
    # Arrange
    handler = MagicMock()
    handler.get_handler.return_value = lambda x: reactivex.just(x)
    handler.get_input_class.return_value = dict
    setup_async_executor_service._AsyncExecutorService__find_handler = MagicMock(
        return_value=handler)
    setup_async_executor_service.execute_with_handler = MagicMock(
        side_effect=Exception("Test Exception"))
    setup_async_executor_service.log.error = MagicMock()

    # Act
    with pytest.raises(Exception):
        setup_async_executor_service._AsyncExecutorService__flat_map(
            setup_exec_dto).subscribe()

    # Assert
    setup_async_executor_service._AsyncExecutorService__find_handler.assert_called_once_with(
        exec_dto=setup_exec_dto)
    setup_async_executor_service.execute_with_handler.assert_called_once_with(
        setup_exec_dto, handler)
    setup_async_executor_service.log.error.assert_called_once_with(
        "Se detecto un error y se detendra la ejecucion del Flux: Test Exception"
    )
