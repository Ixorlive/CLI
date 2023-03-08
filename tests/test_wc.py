from io import StringIO

import pytest

from command.wc import FileResult, TextResult, Wc


@pytest.mark.parametrize(
    "input_text, expected_result",
    [
        ("hello", TextResult(0, 1, 5)),
        ("hello world\nhow are you?", TextResult(1, 5, 24)),
        (
            "We are the chosen ones, we sacrifice our blood We kill for honour",
            TextResult(0, 13, 65),
        ),
    ],
)
def test_wc_base(input_text: str, expected_result: TextResult):
    result = Wc()._wc_base(input_text)
    assert result.count_lines == expected_result.count_lines
    assert result.count_words == expected_result.count_words


@pytest.mark.parametrize(
    "input_files, expected_result",
    [
        (
            ["tests/data/empty.txt"],
            [FileResult("tests/data/empty.txt", TextResult(0, 0, 0))],
        ),
        (
            ["tests/data/text1.txt"],
            [FileResult("tests/data/text1.txt", TextResult(19, 641, 4039))],
        ),
        (
            ["tests/data/big_text.txt"],
            [FileResult("tests/data/big_text.txt", TextResult(13, 379, 2053))],
        ),
        (
            ["tests/data/empty.txt", "tests/data/text1.txt", "tests/data/big_text.txt"],
            [
                FileResult("tests/data/empty.txt", TextResult(0, 0, 0)),
                FileResult("tests/data/text1.txt", TextResult(19, 641, 4039)),
                FileResult("tests/data/big_text.txt", TextResult(13, 379, 2053)),
                FileResult("total", TextResult(32, 1020, 6092)),
            ],
        ),
    ],
)
def test_wc_files(input_files, expected_result):
    assert Wc()._wc_files(input_files) == expected_result


@pytest.mark.parametrize(
    "args, input_text, expected_output",
    [
        ([], "hello world\nhow are you?", "      1       5      24\n"),
        ([], "", "      0       0       0\n"),
        ([], "one\nline\nfile\n", "      3       3      14\n"),
        (["tests/data/big_text.txt"], "", "  13  379 2053 tests/data/big_text.txt\n"),
        (["not_found.txt"], "", "wc: not_found.txt: No such file or directory\n"),
        (
            ["tests/data/text1.txt", "tests/data/cat_data.txt"],
            "",
            "  19  641 4039 tests/data/text1.txt\n"
            "   2    2    8 tests/data/cat_data.txt\n"
            "  21  643 4047 total\n",
        ),
        (
            ["tests/data/big_text.txt", "not_found"],
            "",
            "  13  379 2053 tests/data/big_text.txt\n"
            "wc: not_found: No such file or directory\n"
            "  13  379 2053 total\n",
        ),
    ],
)
def test_wc_execute_text(args, input_text, expected_output):
    """ """
    output_stream = StringIO()
    Wc().execute(
        args,
        input_stream=StringIO(input_text),
        output_stream=output_stream,
        error_stream=StringIO(),
    )
    assert output_stream.getvalue() == expected_output
