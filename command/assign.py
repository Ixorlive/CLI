from command.command_base import *
from environment.context_provider import ContextProvider


class Assign(CommandBase):
    def __init__(
        self, var_name: str, var_value: str, context_provider: ContextProvider
    ):
        self._var_name = var_name
        self._var_value = var_value
        self._context_provider = context_provider

    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ) -> int:
        self._context_provider.set_variable(self._var_name, self._var_value)
        return CODE_OK
