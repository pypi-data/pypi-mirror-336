import pytest
from faker import Faker
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
from boto3 import Session

from arq_base_python.adapters.aws.src.aws_sns_init import AwsSNSInit
from arq_base_python.cqrs.core_api.src.properties.destinations import Destinations


fake = Faker()


@pytest.fixture()
def setup_mq_destinations():
    return MagicMock(spec=Destinations)


@pytest.fixture()
def setup_session():
    return MagicMock(spec=Session)


@pytest.fixture()
def setup_aws_sns_init(setup_session, setup_mq_destinations):
    aws_sns_init = AwsSNSInit(
        aws_session=setup_session, destinations=setup_mq_destinations)
    return aws_sns_init


def test_validate_aws_session(setup_aws_sns_init):
    assert setup_aws_sns_init.validate_aws_session() is None


def test_setup(setup_aws_sns_init):
    assert setup_aws_sns_init


def test_get_topics(setup_aws_sns_init):
    assert isinstance(setup_aws_sns_init._get_topics(), dict)


def test_initialize_topic(setup_aws_sns_init):
    assert setup_aws_sns_init._initialize_topic() is None


def test_validate_aws_session_valid(setup_aws_sns_init, setup_session):
    # Arrange
    sts_client_mock = MagicMock()
    sts_client_mock.get_caller_identity.return_value = {
        'UserId': 'test_user_id',
        'Arn': 'arn:aws:sts::123456789012:user/test_user'
    }
    setup_session.client.return_value = sts_client_mock

    # Act
    setup_aws_sns_init.validate_aws_session()

    # Assert
    sts_client_mock.get_caller_identity.assert_has_calls(
        [MagicMock(), MagicMock()])
    setup_session.client.assert_called_with('sts')


def test_validate_aws_session_invalid_token(setup_aws_sns_init, setup_session):
    # Arrange
    sts_client_mock = MagicMock()
    sts_client_mock.get_caller_identity.side_effect = ClientError(
        {'Error': {'Code': 'InvalidClientTokenId'}}, 'GetCallerIdentity')
    setup_session.client.return_value = sts_client_mock

    # Act and Assert
    with pytest.raises(ValueError, match="Las credenciales de AWS son inválidas"):
        setup_aws_sns_init.validate_aws_session()


def test_validate_aws_session_expired_token(setup_aws_sns_init, setup_session):
    # Arrange
    sts_client_mock = MagicMock()
    sts_client_mock.get_caller_identity.side_effect = ClientError(
        {'Error': {'Code': 'ExpiredToken'}}, 'GetCallerIdentity')
    setup_session.client.return_value = sts_client_mock

    # Act and Assert
    with pytest.raises(ValueError, match="Las credenciales de AWS han expirado"):
        setup_aws_sns_init.validate_aws_session()


def test_validate_aws_session_access_denied(setup_aws_sns_init, setup_session):
    # Arrange
    sts_client_mock = MagicMock()
    sts_client_mock.get_caller_identity.side_effect = ClientError(
        {'Error': {'Code': 'AccessDenied'}}, 'GetCallerIdentity')
    setup_session.client.return_value = sts_client_mock

    # Act and Assert
    with pytest.raises(ValueError, match="El usuario no tiene permisos para acceder a AWS"):
        setup_aws_sns_init.validate_aws_session()


def test_validate_aws_session_other_error(setup_aws_sns_init, setup_session):
    # Arrange
    sts_client_mock = MagicMock()
    sts_client_mock.get_caller_identity.side_effect = ClientError(
        {'Error': {'Code': 'SomeOtherError'}}, 'GetCallerIdentity')
    setup_session.client.return_value = sts_client_mock

    # Act and Assert
    with pytest.raises(ClientError):
        setup_aws_sns_init.validate_aws_session()


def test_get_topics(setup_aws_sns_init, setup_mq_destinations):
    # Arrange
    setup_mq_destinations.get_publish_destination.return_value = "publish_topic"

    # Act
    topics = setup_aws_sns_init._get_topics()

    # Assert
    assert topics == {"publish_topic": False}


def test_initialize_topic_existing(setup_aws_sns_init, setup_session):
    # Arrange
    sns_client_mock = MagicMock()
    sns_client_mock.get_topic_attributes.return_value = {}
    setup_session.client.return_value = sns_client_mock
    setup_session.client('sts').get_caller_identity.return_value = {
        'Account': '123456789012'}
    setup_session.region_name = 'us-east-1'
    setup_aws_sns_init._dict_topics = {"existing_topic": False}

    # Act
    setup_aws_sns_init._initialize_topic()

    # Assert
    sns_client_mock.get_topic_attributes.assert_called_once_with(
        TopicArn='arn:aws:sns:us-east-1:123456789012:existing_topic')
    assert setup_aws_sns_init._dict_topics["existing_topic"] is True


def test_initialize_topic_not_found(setup_aws_sns_init, setup_session):
    # Arrange
    sns_client_mock = MagicMock()
    sns_client_mock.get_topic_attributes.side_effect = ClientError(
        {'Error': {'Code': 'NotFound'}}, 'GetTopicAttributes')
    setup_session.client.return_value = sns_client_mock
    setup_session.client('sts').get_caller_identity.return_value = {
        'Account': '123456789012'}
    setup_session.region_name = 'us-east-1'
    setup_aws_sns_init._dict_topics = {"non_existing_topic": False}

    # Act and Assert
    with pytest.raises(ValueError, match="El tópico non_existing_topic no existe"):
        setup_aws_sns_init._initialize_topic()


def test_initialize_topic_authorization_error(setup_aws_sns_init, setup_session):
    # Arrange
    sns_client_mock = MagicMock()
    sns_client_mock.get_topic_attributes.side_effect = ClientError(
        {'Error': {'Code': 'AuthorizationError'}}, 'GetTopicAttributes')
    setup_session.client.return_value = sns_client_mock
    setup_session.client('sts').get_caller_identity.return_value = {
        'Account': '123456789012'}
    setup_session.region_name = 'us-east-1'
    setup_aws_sns_init._dict_topics = {"unauthorized_topic": False}

    # Act and Assert
    with pytest.raises(ValueError, match="El usuario no tiene permisos para acceder al tópico unauthorized_topic"):
        setup_aws_sns_init._initialize_topic()


def test_initialize_topic_invalid_parameter(setup_aws_sns_init, setup_session):
    # Arrange
    sns_client_mock = MagicMock()
    sns_client_mock.get_topic_attributes.side_effect = ClientError(
        {'Error': {'Code': 'InvalidParameter'}}, 'GetTopicAttributes')
    setup_session.client.return_value = sns_client_mock
    setup_session.client('sts').get_caller_identity.return_value = {
        'Account': '123456789012'}
    setup_session.region_name = 'us-east-1'
    setup_aws_sns_init._dict_topics = {"invalid_topic": False}

    # Act and Assert
    with pytest.raises(ValueError, match="El ARN del tópico invalid_topic es inválido"):
        setup_aws_sns_init._initialize_topic()


def test_initialize_topic_other_error(setup_aws_sns_init, setup_session):
    # Arrange
    sns_client_mock = MagicMock()
    sns_client_mock.get_topic_attributes.side_effect = ClientError(
        {'Error': {'Code': 'SomeOtherError'}}, 'GetTopicAttributes')
    setup_session.client.return_value = sns_client_mock
    setup_session.client('sts').get_caller_identity.return_value = {
        'Account': '123456789012'}
    setup_session.region_name = 'us-east-1'
    setup_aws_sns_init._dict_topics = {"some_topic": False}

    # Act and Assert
    with pytest.raises(ClientError):
        setup_aws_sns_init._initialize_topic()
