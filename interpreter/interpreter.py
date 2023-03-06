from command.parser import Parser
from command.lexer import Lexer
from executor.executor import Executor


class Interpreter:
    # TODO название parser все-таки слишком отсылает к синтаксическому
    #  анализу при этом нельзя сказать, что parser ничего
    #  не делает кроме синтаксического анализа. Возможно стоит вернуться
    #  к старому названию CommandReader? - да не пофиг?
    def __init__(self, executor: Executor):
        # TODO: На схеме Iterpreter не владеет Executor, он его использует
        self._executor = executor

    def run(self):
        # TODO еще над этим циклом и как из него выходить
        # TODO возможно стоит читать строчку аргумент пока кавычки не закрыты?
        while True:
            print("$ ", end="")
            command_line = input()
            # preprocessing
            lexer = Lexer(command_line)
            commands = Parser(lexer).parse_program()
            # TODO: вот так
            result = self._executor.execute(commands)
            if result:
                return
            print()
