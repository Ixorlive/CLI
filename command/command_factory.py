from command import commands


class CommandFactory:
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
            return commands.Assign(var_name=args["var_name"], var_value=args["var_value"])
        return commands.External(command_name)
