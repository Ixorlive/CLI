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
