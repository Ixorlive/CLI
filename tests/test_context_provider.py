from environment.context_provider import ContextProvider


def test_set_and_get_variables():
    context_provider = ContextProvider()
    assert context_provider.get_variable("PATH") is not None
    var_name = "AAAA"
    var_value = "BBBB"
    context_provider.set_variable(var_name, var_value)
    assert context_provider.get_variable(var_name) == var_value


def test_no_found_variables():
    context_provider = ContextProvider()
    assert context_provider.get_variable("test") is None
    context_provider.set_variable("test", "asd")
    assert context_provider.get_variable("test") is not None
