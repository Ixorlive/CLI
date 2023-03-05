from command import commands


class CommandFactory:
    def create_command_base(self, command_name: str) -> commands.CommandBase:
        if command_name == "cat":
            return commands.Cat()
        elif command_name == "echo":
            return commands.Echo()
        elif command_name == "wc":
            return commands.Wc()
        elif command_name == "pwd":
            return commands.Pwd()
        return commands.External(command_name)
