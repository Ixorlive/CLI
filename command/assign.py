import io
from command.command_base import CommandBase
from typing import List
from environment.context_provider import ContextProvider


class Assign(CommandBase):
    def __init__(self, context: ContextProvider, var_name: str, var_value: str):
        self.context = context
        self.var_name = var_name
        self.var_value = var_value

    def execute(
            self,
            args: List[str],
            input_stream: io.StringIO,
            output_stream: io.StringIO,
            error_stream: io.StringIO,
    ):
        self.context.set_variable(self.var_name, self.var_value)