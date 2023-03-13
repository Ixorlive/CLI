import pytest
from parsing.preprocessing import Preprocessor
from environment.context_provider import ContextProvider


def test_simple_substitution():
    cp = ContextProvider()
    cp.set_variable("name", "Alice")
    cp.set_variable("age", "25")
    pp = Preprocessor(cp)
    input_line = "My name is $name and I am $age years old"
    expected_output = "My name is Alice and I am 25 years old"
    assert pp.preprocess(input_line) == expected_output


def test_simple_in_single_quotes():
    cp = ContextProvider()
    pp = Preprocessor(cp)
    input_line = "My name is '$name' and I am '$age' years old"
    expected_output = "My name is '$name' and I am '$age' years old"
    assert pp.preprocess(input_line) == expected_output


def test_simple_back_slash():
    cp = ContextProvider()
    cp.set_variable("name", "Alice")
    pp = Preprocessor(cp)
    input_line = "My name is \\$name"
    expected_output = "My name is $name"
    assert pp.preprocess(input_line) == expected_output


@pytest.mark.parametrize(
    "input_line, expected_line",
    [
        (
            'echo "$test,abc,$test_t asdf,$test12_"',
            'echo "hello,abc,hello1 asdf,hello2"',
        ),
        ("echo '$test, $test_t' $test12_", "echo '$test, $test_t' hello2"),
        ('echo "$123"', 'echo "23"'),
        ('echo "hello $ asdf"', 'echo "hello $ asdf"'),
        ('echo "$test$"', 'echo "hello$"'),
        # no support substitutions yet =(
        # ("echo \"${test}abc${test_t} asdf ${test12_}\"", "echo \"helloabchello1 asdf hello2\""),
        # ("echo \"$test${test_t}$test12_\"", "echo \"hellohello1hello2\""),
        # ("echo \"$test+${test_t}_$test12_\"", "echo \"hello+hello1_hello2\""),
        # ("echo '$test+${test_t}_$test12_'", "echo '$test+${test_t}_$test12_'"),
        ('echo "$test\'s $test12_"', 'echo "hello\'s hello2"'),
        ("echo '\"$test\" is a test'", "echo '\"$test\" is a test'"),
        ("echo 'test \\$test'", "echo 'test \\$test'"),
        ('echo "test \\$test"', 'echo "test $test"'),
        (
            "echo \"single '$test' quotes '$test_t' inside double '$test12_'\"",
            "echo \"single 'hello' quotes 'hello1' inside double 'hello2'\"",
        ),
        (
            'echo \'double "$test" quotes "$test_t" inside single "$test12_"\'"',
            'echo \'double "$test" quotes "$test_t" inside single "$test12_"\'"',
        ),
    ],
)
def test_preprocessor(input_line: str, expected_line: str):
    context: ContextProvider = ContextProvider()
    context.set_variable("test", "hello")
    context.set_variable("test_t", "hello1")
    context.set_variable("test12_", "hello2")
    ps = Preprocessor(context)
    assert ps.preprocess(input_line) == expected_line
