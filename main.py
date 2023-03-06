from executor.executor import Executor
from interpreter.interpreter import Interpreter

if __name__ == "__main__":
    executor = Executor()
    interpreter = Interpreter(executor)
    interpreter.run()
