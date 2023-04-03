import os
from command.command_base import *
import columnify


class Ls(CommandBase):
    """
        A class that implements the 'ls' command.
    """

    def execute(
            self,
            args: List[str],
            input_stream: TextIO,
            output_stream: TextIO,
            error_stream: TextIO,
    ):
        """
        List  information  about  the  FILEs (the current directory by default).
        Args:
            args: A list of command arguments.
            input_stream: The input stream to read from.
            output_stream: The output stream to write to.
            error_stream: The error stream to write to.

        Returns:
            A status code representing the result of the command execution.
        """
        if not args:
            files = self._listdir_nohidden(os.getcwd())
            self._get_formatted_files(files, output_stream)
        else:
            for filename in args:
                if not os.path.exists(filename):
                    output_stream.write(f"ls: cannot access '{filename}': No such file or directory\n")
                    continue

                files = self._listdir_nohidden(filename)
                self._get_formatted_files(files, output_stream, filename)

        return CODE_OK

    def _get_formatted_files(self, files, output_stream, filename=''):
        files.sort(key=str.casefold)
        if filename != '':
            output_stream.write(filename + ':\n')
        output_stream.write(columnify.columnify(files, 80, indent=1))
        output_stream.write('\n')

    def _listdir_nohidden(self, path):
        result = []
        for f in os.listdir(path):
            if not f.startswith('.'):
                result.append(f)

        return result
