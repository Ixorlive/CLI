from parsing.parser import Parser
from parsing.lexer import Lexer
from executor.executor import Executor
from environment.context_provider import ContextProvider
from command.command_factory import CommandFactory


class Interpreter:
    def __init__(self, context: ContextProvider, executor: Executor):
        self._executor = executor
        self.context_provider = context
        self.command_factory = CommandFactory(self.context_provider)

    def run(self):
        while True:
            print("$ ", end="")
            command_line = input()
            # preprocessing
            lexer = Lexer(command_line)
            commands = Parser(self.command_factory, lexer).parse_program()
            # TODO: return false if command is "exit"
            result = self._executor.execute(commands)
            if result:
                return
            print()
