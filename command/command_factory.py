from command import commands
from environment.context_provider import ContextProvider


class CommandFactory:
    """
    The class implements the creation of commands
    """

    def __init__(self, context_provider: ContextProvider):
        self._context_provider = context_provider

    def create_command_base(self, command_name: str, **args) -> commands.CommandBase:
        """
        Create a CommandBase object based on the given command name and arguments.

        Args:
            command_name (str): The name of the command to create.
            **args: Any additional arguments needed to create the command.

        Returns:
            CommandBase: The created CommandBase object.
        """
        if command_name == "cat":
            return commands.Cat()
        elif command_name == "echo":
            return commands.Echo()
        elif command_name == "wc":
            return commands.Wc()
        elif command_name == "pwd":
            return commands.Pwd()
        elif command_name == "grep":
            return commands.Grep()
        elif command_name == "exit":
            return commands.Exit()
        elif command_name == "=":
            return commands.Assign(
                var_name=args["var_name"],
                var_value=args["var_value"],
                context_provider=self._context_provider,
            )
        return commands.External(command_name)
