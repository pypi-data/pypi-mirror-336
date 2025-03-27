# import random

import pytest

# from faker import Faker

from entrypoints_base.command_receiver.src.commands.invalid_regex import (
    InvalidRegex,
)

# from entrypoints_command_receiver.tests import support_data


# fake = Faker()


@pytest.fixture()
def setup_invalid_regex():
    invalid_regex = InvalidRegex(default_regex={})
    return invalid_regex


@pytest.fixture
def invalid_regex():
    default_regex = {
        "id": "~!@#&|;'?'/*$^+<>",
        "nombre": "~!@#&|;'?'/*$^+<>",
    }
    return InvalidRegex(default_regex=default_regex)


def test_print_regex(invalid_regex):
    expected_output = {
        "id": "[~!@#&|;'?'/*$^+<>]",
        "nombre": "[~!@#&|;'?'/*$^+<>]",
        "id_trazabilidad": InvalidRegex.global_regex,
        "version": InvalidRegex.global_regex,
        "aplicacion_emisora": InvalidRegex.global_regex,
        "aplicacion_origen": InvalidRegex.global_regex,
        "usuario": InvalidRegex.global_regex,
        "dni": InvalidRegex.global_regex,
        "timestamp": InvalidRegex.global_regex,
        "payload": InvalidRegex.global_regex,
        "default_regex": invalid_regex.default_regex,
    }
    assert invalid_regex.print_regex() == expected_output


def test_get_regex(invalid_regex):
    assert invalid_regex.get_regex("id") == "[~!@#&|;'?'/*$^+<>]"
    assert invalid_regex.get_regex("nombre") == "[~!@#&|;'?'/*$^+<>]"
    assert invalid_regex.get_regex(
        "id_trazabilidad") == InvalidRegex.global_regex
    assert invalid_regex.get_regex("version") == InvalidRegex.global_regex
    assert invalid_regex.get_regex(
        "aplicacion_emisora") == InvalidRegex.global_regex
    assert invalid_regex.get_regex(
        "aplicacion_origen") == InvalidRegex.global_regex
    assert invalid_regex.get_regex("usuario") == InvalidRegex.global_regex
    assert invalid_regex.get_regex("dni") == InvalidRegex.global_regex
    assert invalid_regex.get_regex("timestamp") == InvalidRegex.global_regex
    assert invalid_regex.get_regex("payload") == InvalidRegex.global_regex


def test_add_brackets(invalid_regex):
    assert invalid_regex._add_brackets(
        "~!@#&|;'?'/*$^+<>") == "[~!@#&|;'?'/*$^+<>]"
    assert (
        invalid_regex._add_brackets(
            r"[~!@#&|;'?/*$^+\\<>]") == r"[~!@#&|;'?/*$^+\\<>]"
    )


def test_invalid_regex(setup_invalid_regex):
    assert setup_invalid_regex


# def test_print_regex(setup_invalid_regex):
#     assert isinstance(setup_invalid_regex.print_regex(), dict)


# def test_get_regex(setup_invalid_regex):
#     assert setup_invalid_regex.get_regex(key=random.choice(support_data.list_regex))
