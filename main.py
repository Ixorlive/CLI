from command.parser import Parser
from command.lexer import Lexer
from command.command_factory import CommandFactory
from executor.executor import Executor
from interpreter.interpreter import Interpreter

if __name__ == "__main__":

    lexer = Lexer()
    command_factory = CommandFactory()
    parser = Parser(command_factory, lexer)

    executor = Executor()
    interpreter = Interpreter(parser, executor)
    interpreter.run()
