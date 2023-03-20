import io
from typing import List

import pytest

from command.grep import Grep


@pytest.fixture
def simple_input() -> str:
    return "hello world\nfoo1 bar\nbar\n"


@pytest.mark.parametrize(
    "input_arg, expected_result",
    [
        (["foo"], "foo1 bar\n"),
        (["foo1", "-w"], "foo1 bar\n"),
        (["-i", "HELLO"], "hello world\n"),
        (["-A", "0", "foo"], "foo1 bar\n"),
        (["-A", "1", "hello"], "hello world\nfoo1 bar\n"),
    ],
)
def test_simple(simple_input, input_arg: List, expected_result: str):
    input_stream = io.StringIO(simple_input)
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    grep = Grep()
    result = grep.execute(input_arg, input_stream, output_stream, error_stream)
    assert result == 0
    assert output_stream.getvalue() == expected_result


@pytest.fixture
def regex_input() -> str:
    return "apple\nbanana\npear\norange\ngrapefruit\n"


@pytest.mark.parametrize(
    "args, expected_output",
    [(["e$"], "apple\norange\n"), (["p.*e"], "apple\npear\ngrapefruit\n")],
)
def test_with_regex(regex_input: str, args: List[str], expected_output: str):
    input_stream = io.StringIO(regex_input)
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    grep = Grep()
    result = grep.execute(args, input_stream, output_stream, error_stream)
    assert result == 0
    assert output_stream.getvalue() == expected_output


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (
            ["-w", "operator", "test/data/grep_test.txt"],
            "concurrent::FunctionId::operator bool() const { return ptr_ != nullptr; }\n"
            "bool FunctionId::operator==(const FunctionId& other) const {\n"
            "std::size_t FunctionId::Hash::operator()(FunctionId id) const noexcept {\n"
            "AsyncEventSubscriberScope& AsyncEventSubscriberScope::operator=(\n",
        ),
        (
            ["t$", "data/grep_test.txt"],
            "    AsyncEventSubscriberScope&& scope) noexcept\n"
            "}  // namespace concurrent\n",
        ),
        (
            ["-i", "namespace", "test/data/grep_test.txt"],
            "USERVER_NAMESPACE_BEGIN\n"
            "namespace concurrent {\n"
            "namespace impl {\n"
            "}  // namespace impl\n"
            "}  // namespace concurrent\n"
            "USERVER_NAMESPACE_END",
        ),
        (
            ["-A", "1", "hash", "test/data/grep_test.txt"],
            "  return std::hash<void*>{}(id.ptr_);\n" "}\n",
        ),
    ],
)
def test_grep_test_txt_file(args, expected_output):
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    error_stream = io.StringIO()
    grep = Grep()
    result = grep.execute(args, input_stream, output_stream, error_stream)
    assert result == 0
    assert output_stream.getvalue() == expected_output
