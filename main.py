from environment.context_provider import ContextProvider
from executor.executor import Executor
from interpreter.interpreter import Interpreter
from command.command_factory import CommandFactory
from parsing.preprocessing import Preprocessor

if __name__ == "__main__":
    context_provider = ContextProvider()
    command_factory = CommandFactory(context_provider)
    preprocessor = Preprocessor(context_provider)
    executor = Executor()
    interpreter = Interpreter(executor, command_factory, preprocessor)
    interpreter.run()
