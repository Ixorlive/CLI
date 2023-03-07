from executor.executor import Executor
from interpreter.interpreter import Interpreter
from environment.context_provider import ContextProvider

if __name__ == "__main__":
    executor = Executor()
    context = ContextProvider()
    interpreter = Interpreter(context, executor)
    interpreter.run()
