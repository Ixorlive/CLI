from typing import NamedTuple

from command.command_base import *


class TextResult(NamedTuple):
    count_lines: int
    count_words: int
    utf8len: int


class FileResult(NamedTuple):
    filename: str
    text_result: TextResult


class Wc(CommandBase):
    def execute(
        self,
        args: List[str],
        input_stream: TextIO,
        output_stream: TextIO,
        error_stream: TextIO,
    ):
        if not args:
            text_statistic = self._wc_base(input_stream.read())
            output_stream.write(
                "{:>7}".format(str(text_statistic.count_lines))
                + "{:>8}".format(str(text_statistic.count_words))
                + "{:>8}".format(str(text_statistic.utf8len))
            )
            output_stream.write("\n")
        else:
            files_statistic = self._wc_files(args)
            # last row is "total" - it have max value -> max len (or result have only one file)
            max_len = (
                len(str(files_statistic[-1].text_result.utf8len))
                if isinstance(files_statistic[-1], FileResult)
                else 0
            )
            for file_statistic in files_statistic:
                if isinstance(file_statistic, str):
                    output_stream.write(file_statistic)
                else:
                    for j in range(3):
                        output_stream.write(
                            f"{file_statistic.text_result[j]:{max_len}} "
                        )
                    output_stream.write(file_statistic.filename)
                output_stream.write("\n")
        return CODE_OK

    def _wc_base(self, text: str) -> TextResult:
        count_lines = text.count("\n")
        count_words = len(text.split())
        utf8_len = len(text.encode("utf-8"))
        return TextResult(count_lines, count_words, utf8_len)

    def _wc_files(self, file_paths: List[str]) -> List[FileResult]:
        all_results = []
        total = [0, 0, 0]
        for file_path in file_paths:
            try:
                with open(file_path, "r") as file:
                    result = self._wc_base(file.read())
                    all_results.append(FileResult(file_path, result))

                    total[0] += result.count_lines
                    total[1] += result.count_words
                    total[2] += result.utf8len
            except FileNotFoundError:
                all_results.append(f"wc: {file_path}: No such file or directory")
        if len(file_paths) > 1:
            all_results.append(
                FileResult("total", TextResult(total[0], total[1], total[2]))
            )
        return all_results
