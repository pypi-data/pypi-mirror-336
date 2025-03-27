import pytest
from arq_base_python.jano.core.src.realm import Realm


@pytest.fixture
def realm():
    return Realm()


def test_initialization(realm):
    assert realm.EMPLEADOS is False
    assert realm.CLIENTE_AFILIADO is False
    assert realm.CLIENTE_EMPRESA is False
    assert realm.TERCERO is False
    assert realm.APLICACION is False


def test_set_empleados(realm):
    realm._Realm__EMPLEADOS = True
    assert realm.EMPLEADOS is True


def test_set_cliente_afiliado(realm):
    realm._Realm__CLIENTE_AFILIADO = True
    assert realm.CLIENTE_AFILIADO is True


def test_set_cliente_empresa(realm):
    realm._Realm__CLIENTE_EMPRESA = True
    assert realm.CLIENTE_EMPRESA is True


def test_set_tercero(realm):
    realm._Realm__TERCERO = True
    assert realm.TERCERO is True


def test_set_aplicacion(realm):
    realm._Realm__APLICACION = True
    assert realm.APLICACION is True
