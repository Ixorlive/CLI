import io
import os

import pytest

from command import commands


@pytest.mark.parametrize(
    "args, expected_output, expected_errors, expected_return_code",
    [
        (["tests/data/cat_data.txt"], "aaa\nbbb\n", "", commands.CODE_OK),
        (
            ["not_file"],
            "",
            "cat: not_file: No such file or directory\n",
            commands.INTERNAL_COMMAND_ERROR,
        ),
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
        ([], os.getcwd() + "\n", commands.CODE_OK),
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


def test_assign(mocker):
    context_provider = mocker.MagicMock()
    var_name = "VAR_NAME"
    var_value = "100"
    context_provider.get_variable.return_value = var_value
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


@pytest.mark.skipif(os.name == "nt", reason="there is no cat on windows")
def test_external_command_executed_successfully():
    command = commands.External("cat")
    args = ["tests/data/cat_data.txt"]
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    result = command.execute(args, input_stream, output_stream, error_stream)
    assert result == commands.CODE_OK
    output_stream.seek(0)
    assert output_stream.read() == "aaa\nbbb\n"
    error_stream.seek(0)
    assert error_stream.read() == ""


@pytest.mark.skipif(os.name == "nt", reason="there is no cat on windows")
def test_external_command_executed_failure():
    command = commands.External("cat")
    args = ["not_file"]
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    result = command.execute(args, input_stream, output_stream, error_stream)
    assert result == 1
    output_stream.seek(0)
    assert output_stream.read() == ""
    error_stream.seek(0)
    assert error_stream.read().startswith("/usr/bin/cat: not_file: ")


@pytest.mark.skipif(os.name != "nt", reason="test for windows")
def test_external_command_executed_successfully():
    command = commands.External("cmd")
    args = ["/c", "path"]
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()

    result = command.execute(args, input_stream, output_stream, error_stream)
    assert result == commands.CODE_OK
    output_stream.seek(0)
    assert output_stream.read().startswith("PATH=")
    error_stream.seek(0)
    assert error_stream.read() == ""
