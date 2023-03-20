from typing import List, TextIO
import io

from command import commands
from executor.executor import Executor


def test_executor(mocker):
    executor = Executor()
    assert executor.execute([]) == commands.CODE_OK
    mock = mocker.MagicMock()

    mock.execute.return_value = commands.CODE_EXIT
    assert executor.execute([mock]) == commands.CODE_EXIT

    mock.execute.return_value = commands.CODE_OK
    assert executor.execute([mock]) == commands.CODE_OK


def test_executor_exit(mocker):
    executor = Executor()
    mock_commands = [mocker.MagicMock() for _ in range(5)]

    for mock in mock_commands:
        mock.execute.return_value = commands.CODE_EXIT
    assert executor.execute(mock_commands) == commands.CODE_OK

    mock_commands[0].execute.return_value = commands.CODE_EXIT
    assert executor.execute(mock_commands) == commands.CODE_OK

    mock_commands[1].execute.return_value = commands.CODE_EXIT
    assert executor.execute(mock_commands) == commands.CODE_OK

    mock_commands[-1].execute.return_value = commands.CODE_EXIT
    assert executor.execute(mock_commands) == commands.CODE_OK
    assert executor.execute(mock_commands[-1:]) == commands.CODE_EXIT


def test_executor_pipes(mocker, monkeypatch, capfd):
    command_number = 5
    commands_input = []
    commands_output = []

    def fake_execute(
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        nonlocal commands_input, commands_output
        input_data = input_stream.read()
        output_data = input_data + "new data\n"
        output_stream.write(output_data)
        commands_input.append(input_data)
        commands_output.append(output_data)
        return commands.CODE_OK

    executor = Executor()
    mock_commands = [mocker.MagicMock() for _ in range(command_number)]
    stdin_data = "stdin_data\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin_data))

    for mock in mock_commands:
        mock.execute = fake_execute

    assert executor.execute(mock_commands) == commands.CODE_OK
    for input_data, output_data in zip(commands_input[1:], commands_output):
        assert input_data == output_data

    out, err = capfd.readouterr()
    assert out == commands_output[-1]
    assert err == ""
