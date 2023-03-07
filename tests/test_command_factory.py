import pytest

from command.command_factory import CommandFactory
from environment.context_provider import ContextProvider
from command import commands


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
def test_create_command_base(command_name, command_base_class, args):
    context_provider = ContextProvider()
    command_factory = CommandFactory(context_provider)
    base = command_factory.create_command_base(command_name, **args)
    assert isinstance(base, command_base_class)
