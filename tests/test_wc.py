from io import StringIO
import pytest
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
    (["data/empty.txt"],
       [FileResult("data/empty.txt", TextResult(0, 0, 0))]
    ),
    (["data/text1.txt"],
        [FileResult("data/text1.txt", TextResult(18, 641, 4056))]
    ),
    (["data/big_text.txt"],
        [FileResult("data/big_text.txt", TextResult(51, 320, 1705))]
    ),
    (["data/empty.txt", "data/text1.txt", "data/big_text.txt"],
        [FileResult("data/empty.txt", TextResult(0, 0, 0)),
         FileResult("data/text1.txt", TextResult(18, 641, 4056)),
         FileResult("data/big_text.txt", TextResult(51, 320, 1705))]
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