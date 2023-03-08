from command.command_base import *
from environment.context_provider import ContextProvider


class Assign(CommandBase):
    """
    Command that adds a variable to the given context.
    """

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
        """
        Executes the Assign command by adding the variable to the context.

        Args:
            args (List[str]): Unused in the Assign command.
            input_stream (TextIO): Unused in the Assign command.
            output_stream (TextIO): Unused in the Assign command.
            error_stream (TextIO): Unused in the Assign command.

        Returns:
            int: The status code for the execution of the Assign command.
        """
        self._context_provider.set_variable(self._var_name, self._var_value)
        return CODE_OK
