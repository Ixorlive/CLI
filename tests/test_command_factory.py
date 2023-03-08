import pytest

from command import commands
from command.command_factory import CommandFactory


@pytest.mark.parametrize(
    "command_name, command_base_class, args",
    [
        ("cat", commands.Cat, {}),
        ("echo", commands.Echo, {}),
        ("wc", commands.Wc, {}),
        ("pwd", commands.Pwd, {}),
        ("exit", commands.Exit, {}),
        ("=", commands.Assign, {"var_name": "NAME", "var_value": "value"}),
        ("bash", commands.External, {}),
    ],
)
def test_create_command_base(mocker, command_name, command_base_class, args):
    context_provider = mocker.MagicMock()
    command_factory = CommandFactory(context_provider)
    base = command_factory.create_command_base(command_name, **args)
    assert isinstance(base, command_base_class)
