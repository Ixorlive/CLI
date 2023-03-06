from command import commands
from environment.context_provider import ContextProvider


class CommandFactory:
    def __init__(self, context_provider: ContextProvider):
        self._context_provider = context_provider

    def create_command_base(self, command_name: str, **args) -> commands.CommandBase:
        if command_name == "cat":
            return commands.Cat()
        elif command_name == "echo":
            return commands.Echo()
        elif command_name == "wc":
            return commands.Wc()
        elif command_name == "pwd":
            return commands.Pwd()
        elif command_name == "=":
            return commands.Assign(
                var_name=args["var_name"],
                var_value=args["var_value"],
                context_provider=self._context_provider,
            )
        return commands.External(command_name)
