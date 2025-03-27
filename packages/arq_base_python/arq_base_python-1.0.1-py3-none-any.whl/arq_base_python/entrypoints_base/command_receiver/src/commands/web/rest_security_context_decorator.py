import logging
import time
import uuid
import re

from reactivex import of, operators as op

from arq_base_python.cqrs.core_api.src.command.security_helper import SecurityHelper
from arq_base_python.cqrs.core_api.src.models.aplicacion_emisora import AplicacionEmisora
from arq_base_python.cqrs.core_api.src.models.aplicacion_origen import AplicacionOrigen
from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted
from arq_base_python.cqrs.core_api.src.models.command import Command
from arq_base_python.cqrs.core_api.src.models.dni import Dni
from arq_base_python.cqrs.core_api.src.models.usuario import Usuario
from arq_base_python.jano.core.src.realm import Realm
from arq_base_python.jano.core.src.request_metadata import RequestMetadata
from arq_base_python.jano.core.src.secured_application import SecuredApplication
from arq_base_python.jano.core.src.header_names import HeaderNames
from arq_base_python.jano.core.src.identity.identificacion import Identificacion
from arq_base_python.jano.core.src.user_properties import UserProperties


class RestSecurityContextDecorator(SecurityHelper):

    def __init__(self, secured_application: SecuredApplication):
        self.secured_application = secured_application
        self.key = ""
        self.request = {}
        self.host = ""
        self.headers = {}
        self.log = logging.getLogger(__name__)

    def enrich_with_security_props(self, command: CommandSubmitted, context: object):
        self.log.debug("Inicializando comando con propiedades de seguridad...")
        request = context

        try:
            command_submitted = of(command)
        except Exception as e:
            self.log.error(f"Se genero un error: {str(e)}")
            command_submitted = of({})

        command_submitted_set_timestamp = self.receive_command_submitted_timestamp_validator(
            observer_object=command_submitted
        )

        command_submitted_set_issuer_app = self.receive_command_submitted_issuer_app_validator(
            observer_object=of(command_submitted_set_timestamp)
        )

        command_submitted_set_issuer_app_data = self.receive_command_submitted_issuer_app_validator_data(
            observer_object=of(command_submitted_set_issuer_app)
        )

        command_submitted_set_command_id = self.receive_command_submitted_command_id_validator(
            observer_object=of(command_submitted_set_issuer_app_data)
        )

        command_submitted_parse_dni = self.receive_command_submitted_command_DNI_validator(
            observer_object=of(command_submitted_set_command_id),
            request=request
        )

        command_data_completed = self.receive_data_validator(
            observer_object=of(command_submitted_parse_dni)
        )
        command_user_data_validator = self.receive_command_user_data_validator(
            observer_object=of(command_data_completed)
        )

        self.log.debug(
            f"Comando despues de inicializacion de propiedades {command_user_data_validator}")

        return command_user_data_validator

    def receive_command_after(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__process_user_data)
        )
        return observer_object

    def __process_command_after(self, commandSubmitted: CommandSubmitted):
        self.log.debug(
            f"Comando despues de inicializacion de propiedades {commandSubmitted}")
        return commandSubmitted

    def receive_command_user_data_validator(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__process_user_data)
        )
        return observer_object.run()

    def __process_user_data(self, commandSubmitted: CommandSubmitted):
        if not commandSubmitted.get().usuario:
            commandSubmitted.get().usuario = Usuario()
            commandSubmitted.get().usuario.dni = "DNI_NO_DISPONIBLE"
            commandSubmitted.get().usuario.nombre = "USUARIO_NO_DISPONIBLE"
            commandSubmitted.get().usuario.id_session = "SESION_NO_DISPONIBLE"
            commandSubmitted.get().usuario.canal = "CANAL_NO_INDICADO"
            commandSubmitted.get().usuario.telefono = "TELEFONO_NO_INDICADO"
            self.log.debug(
                f"Usuario era nulo, inicializado {commandSubmitted.get().usuario}")
        return commandSubmitted

    def receive_data_validator(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__process_data)
        )
        return observer_object.run()

    def __process_data(self, observable_object):
        new_observable_object = of(observable_object)

        observer_object = new_observable_object.pipe(
            op.map(self.__parseJanoProperties)
        )
        return observer_object.run()

    def __parseJanoProperties(self, command):

        request_meta_data = self.__getPrincipal()

        if command.get().usuario is None:
            self.log.debug(
                "Datos de Usuario no detectado en el comando, inicializando.")
            command.get().usuario = Usuario()

        userProperties = request_meta_data.userProperties
        command.get().usuario.dni = str(userProperties.identificacion)
        command.get().usuario.nombre = userProperties.subject
        command.get().usuario.ip = userProperties.ipAddress
        command = self.__parseUuidSession(
            command=command, userProperties=userProperties)
        command = self.__parseCanal(command=command)

        if not command.get().usuario.telefono:
            command.get().usuario.telefono = "TELEFONO_NO_INDICADO"

        return command

    def __parseCanal(self, command: CommandSubmitted):
        canalHeader = self.headers.get("canal")
        if not command.get().usuario.canal and canalHeader:
            command.get().usuario.canal = canalHeader
        else:
            command.get().usuario.canal = "CANAL_NO_INDICADO"
        return command

    def __parseUuidSession(self, command: CommandSubmitted, userProperties: UserProperties):
        if not userProperties.realm:
            command.get().usuario.id_session = "SESION_NO_DISPONIBLE"
        else:
            realm = Realm()
            isUserToken = realm.CLIENTE_AFILIADO or realm.CLIENTE_EMPRESA or realm.EMPLEADOS
            if isUserToken and userProperties.uuidSession is not None:
                command.get().usuario.id_session = userProperties.uuidSession
            if not command.get().usuario.id_session:
                command.get().usuario.id_session = "SESION_NO_DISPONIBLE"
        return command

    def __getPrincipal(self):
        if self.secured_application.jano_enabled:
            # TODO: Make logic when jano is enabled
            # return request.principal()
            # Probably request doesn't have principal method
            pass
        else:
            self.log.debug(
                "Jano no esta habilitado. Se asumira identidad ANONIMA!")
            # UsernamePasswordAuthenticationToken tk = new UsernamePasswordAuthenticationToken("anonymous", UUID.randomUUID().toString());
            requestMetadata: RequestMetadata = RequestMetadata()
            userProperties: UserProperties = UserProperties()

            userProperties.groups = []
            userProperties.roles = []
            userProperties.subject = "anonymous"
            userProperties.accountEnabled = True
            userProperties.identificacion = Identificacion(
                id="00000", tipoId="XX")
            userProperties.nivelSeguridad = 5

            ip: str = self.host.split(":")[0] if self.host else "x.x.x.x"
            userProperties.ipAddress = ip
            userProperties.displayName = "Usuario Anonimo Jano No Activado"
            userProperties.givenName = "Jano No activado"
            userProperties.surName = "Usuario Anonimo"
            requestMetadata.userProperties = userProperties

            return requestMetadata

    def receive_command_submitted_command_DNI_validator(self, observer_object, request):
        self.host = request.client.host
        self.headers = request.headers
        self.request = request

        observer_object = observer_object.pipe(
            op.map(self.__set_dni_data)
        )

        return observer_object.run()

    def __set_dni_data(self, commandSubmitted):
        commandSubmitted = self.__parseClienteDNI(commandSubmitted)
        return commandSubmitted

    @staticmethod
    def __filter_request_headers(pair):
        key, value = pair
        if key.lower() == "ClienteDNI".lower() or key.lower() == HeaderNames.HEADER_CLIENTE_DNI_MIN.lower():
            return key
        else:
            return ""

    def __parseClienteDNI(self, command):
        try:
            headers_observable = of(self.headers)
        except Exception as e:
            self.log.debug(str(e))
            headers_observable = of({})

        key = self.receive_headers_observable(
            headers_observable=headers_observable
        )

        header_list = self.receive_filtered_headers_observable(
            observable_object=headers_observable,
            key=key
        )

        cleaned_header_list = self.received_filter_by_key_headers_observable(
            observable_object=of(header_list)
        )

        header = self.receive_filtered_not_empty_headers(
            observable_object=of(cleaned_header_list)
        )

        dni = self.receive_header_observable(
            observable_object=of(header)
        )
        command.get().dni = dni

        return command

    def receive_header_observable(self, observable_object):
        observer_object = observable_object.pipe(
            op.map(self.__process_header)
        )
        result = observer_object.run()
        return result

    def __process_header(self, header_value):
        match_result = re.match(
            Identificacion.IDENTIFICACION_PATTERN, header_value)
        if match_result:
            dni1: Dni = Dni()
            dni1.identificacion = match_result[3]
            dni1.tipo_identificacion = match_result[1]
            return dni1
        else:
            self.log.error(
                "No se encontro informacion valida en el encabezado ClienteDNI")
            return Dni()

    def receive_filtered_not_empty_headers(self, observable_object):
        observer_object = observable_object.pipe(
            op.map(self.__take_first_element)
        )
        first_element = observer_object.run()
        return first_element

    @staticmethod
    def __take_first_element(observable_list):
        if observable_list:
            return observable_list[0]
        else:
            return ""

    def received_filter_by_key_headers_observable(self, observable_object):
        observer_object = observable_object.pipe(
            op.map(self.__filter_empty_headers)
        )
        cleaned_headers = observer_object.run()
        return cleaned_headers

    def __filter_empty_headers(self, observable_headers):
        return [h for h in observable_headers if h]

    def receive_filtered_headers_observable(self, observable_object, key):
        self.key = key

        observer_object = observable_object.pipe(
            op.map(self.__filter_headers_by_key)
        )

        result = observer_object.run()

        if result:
            return [result]
        else:
            return []

    def __filter_headers_by_key(self, observable_object):
        return {i[0]: i[1] for i in observable_object.items()}.get(self.key)

    def receive_headers_observable(self, headers_observable):
        observer_object = headers_observable.pipe(
            op.map(self.__filter_headers)
        )
        key = observer_object.run()

        if key:
            return key[0][0]
        else:
            return ''

    def __filter_headers(self, headers_observable):
        key = list(filter(self.__filter_request_headers, {
                   i[0]: i[1] for i in headers_observable.items()}.items()))
        return key

    def receive_command_submitted_command_id_validator(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__set_command_id_data)
        )
        return observer_object.run()

    def __set_command_id_data(self, commandSubmitted: CommandSubmitted) -> CommandSubmitted:
        if not commandSubmitted.get().id:
            self.log.debug("ID del comando es vacio, estableciendo un ID")
            commandSubmitted.get().id = str(uuid.uuid4())
        return commandSubmitted

    def receive_command_submitted_issuer_app_validator_data(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__set_issuer_app_data)
        )
        return observer_object.run()

    def __set_issuer_app_data(self, commandSubmitted: CommandSubmitted) -> CommandSubmitted:
        commandSubmitted.get().aplicacion_origen.nombre_aplicacion_origen = self.secured_application.name if not commandSubmitted.get(
        ).aplicacion_emisora.nombre_aplicacion_emisora else commandSubmitted.get().aplicacion_emisora.nombre_aplicacion_emisora
        commandSubmitted.get().aplicacion_origen.id_aplicacion_origen = str(self.secured_application.id_app_proteccion) if not commandSubmitted.get(
        ).aplicacion_emisora.id_aplicacion_emisora else str(commandSubmitted.get().aplicacion_emisora.id_aplicacion_emisora)
        commandSubmitted.get().aplicacion_emisora.id_aplicacion_emisora = str(
            self.secured_application.id_app_proteccion)
        commandSubmitted.get(
        ).aplicacion_emisora.nombre_aplicacion_emisora = self.secured_application.name
        return commandSubmitted

    def receive_command_submitted_issuer_app_validator(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__set_issuer_app)
        )
        return observer_object.run()

    @staticmethod
    def __set_issuer_app(commandSubmitted: CommandSubmitted) -> CommandSubmitted:
        if commandSubmitted.get().aplicacion_emisora is None:
            commandSubmitted.get().aplicacion_emisora = AplicacionEmisora()

        commandSubmitted.get().aplicacion_origen = AplicacionOrigen()
        return commandSubmitted

    def receive_command_submitted_timestamp_validator(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self.__set_timestamp)
        )
        return observer_object.run()

    @staticmethod
    def __set_timestamp(commandSubmitted: CommandSubmitted) -> CommandSubmitted:
        if commandSubmitted.get().timestamp is None or commandSubmitted.get().timestamp <= 0:
            commandSubmitted.get().timestamp = time.time()
        return commandSubmitted
