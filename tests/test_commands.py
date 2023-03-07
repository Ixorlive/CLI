import os

import pytest
import io

from command import commands
from environment.context_provider import ContextProvider


@pytest.mark.parametrize(
    "args, expected_output, expected_errors, expected_return_code",
    [
        ([], "", "cat: file not specified\n", commands.INTERNAL_COMMAND_ERROR),
        (["data/cat_data.txt"], "aaa\nbbb\n", "", commands.CODE_OK),
    ],
)
def test_cat(args, expected_output, expected_errors, expected_return_code):
    command = commands.Cat()
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    assert (
        command.execute(args, input_stream, output_stream, error_stream)
        == expected_return_code
    )
    output_stream.seek(0)
    assert output_stream.read() == expected_output
    error_stream.seek(0)
    assert error_stream.read() == expected_errors


@pytest.mark.parametrize(
    "args, expected_output, expected_return_code",
    [
        ([], "\n", commands.CODE_OK),
        (["aaaaaa"], "aaaaaa\n", commands.CODE_OK),
        (["aaaaaa", "bbbbbb"], "aaaaaa bbbbbb\n", commands.CODE_OK),
    ],
)
def test_echo(args, expected_output, expected_return_code):
    command = commands.Echo()
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    assert (
        command.execute(args, input_stream, output_stream, error_stream)
        == expected_return_code
    )
    output_stream.seek(0)
    assert output_stream.read() == expected_output
    error_stream.seek(0)
    assert error_stream.readline() == ""


@pytest.mark.parametrize(
    "args, expected_output, expected_return_code",
    [
        ([], os.getcwd(), commands.CODE_OK),
    ],
)
def test_pwd(args, expected_output, expected_return_code):
    command = commands.Pwd()
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    assert (
        command.execute(args, input_stream, output_stream, error_stream)
        == expected_return_code
    )
    output_stream.seek(0)
    assert output_stream.read() == expected_output
    error_stream.seek(0)
    assert error_stream.readline() == ""


def test_exit():
    command = commands.Exit()
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    assert (
        command.execute([], input_stream, output_stream, error_stream)
        == commands.CODE_EXIT
    )
    output_stream.seek(0)
    assert output_stream.read() == ""
    error_stream.seek(0)
    assert error_stream.readline() == ""


def test_assign():
    context_provider = ContextProvider()
    var_name = "VAR_NAME"
    var_value = "100"
    command = commands.Assign(var_name, var_value, context_provider)
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    assert (
        command.execute([], input_stream, output_stream, error_stream)
        == commands.CODE_OK
    )
    assert context_provider.get_variable(var_name) == var_value
    output_stream.seek(0)
    assert output_stream.read() == ""
    error_stream.seek(0)
    assert error_stream.readline() == ""
