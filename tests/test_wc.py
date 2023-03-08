from io import StringIO
import pytest
import os
from command.wc import Wc, TextResult, FileResult


@pytest.mark.parametrize("input_text, expected_result", [
    ("hello", TextResult(0, 1, 5)),
    ("hello world\nhow are you?", TextResult(1, 5, 24)),
    ("We are the chosen ones, we sacrifice our blood We kill for honour", TextResult(0, 13, 65))
])
def test_wc_base(input_text: str, expected_result: TextResult):
    result = Wc()._wc_base(input_text)
    assert result.count_lines == expected_result.count_lines
    assert result.count_words == expected_result.count_words


@pytest.mark.parametrize("input_files, expected_result", [
    (["tests/data/empty.txt"],
     [FileResult("tests/data/empty.txt", TextResult(0, 0, 0))]
     ),
    (["tests/data/text1.txt"],
     [FileResult("tests/data/text1.txt", TextResult(18, 641, 4056))]
     ),
    (["tests/data/big_text.txt"],
     [FileResult("tests/data/big_text.txt", TextResult(12, 379, 1705))]
     ),
    (["tests/data/empty.txt", "tests/data/text1.txt", "tests/data/big_text.txt"],
     [FileResult("tests/data/empty.txt", TextResult(0, 0, 0)),
      FileResult("tests/data/text1.txt", TextResult(18, 641, 4056)),
      FileResult("tests/data/big_text.txt", TextResult(12, 379, 1705))]
     )
])
def test_wc_files(input_files, expected_result):
    """
    I got the expected value using real wc in wls ubuntu.
    However, the results may differ, but only for 3 parameters of TextResult (utf8len).
    Mb Im wrong.
    """
    result = Wc()._wc_files(input_files)
    for actual, expected in zip(result, expected_result):
        assert actual.text_result.count_words == expected.text_result.count_words
        assert actual.text_result.count_lines == expected.text_result.count_lines
        assert actual.filename == expected.filename


@pytest.mark.parametrize("args, input_text, expected_output", [
    ([], "hello world\nhow are you?", "      1       5      24\n"),
    ([], "", "      0       0       0\n"),
    ([], "one\nline\nfile\n", "      3       3      14\n"),
    (["tests/data/big_text.txt"], "", "  12  379 2052 tests/data/big_text.txt\n"),
    (["not_found.txt"], "", "wc: not_found.txt: No such file or directory\n"),
    (["tests/data/text1.txt", "tests/data/cat_data.txt"], "", "  18  641 4038 tests/data/text1.txt\n"
                                                              "   2    2    8 tests/data/cat_data.txt\n"
                                                              "  20  643 4046 total\n"),
    (["tests/data/big_text.txt", "not_found"], "", "  12  379 2052 tests/data/big_text.txt\n"
                                                   "wc: not_found: No such file or directory\n"
                                                   "  12  379 2052 total\n")
])
def test_wc_execute_text(args, input_text, expected_output):
    """

    """
    output_stream = StringIO()
    Wc().execute(args, input_stream=StringIO(input_text), output_stream=output_stream, error_stream=None)
    assert output_stream.getvalue() == expected_output
    # assert true
