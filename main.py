from environment.context_provider import ContextProvider
from executor.executor import Executor
from interpreter.interpreter import Interpreter

if __name__ == "__main__":
    context_provider = ContextProvider()
    executor = Executor()
    interpreter = Interpreter(executor, context_provider)
    interpreter.run()
