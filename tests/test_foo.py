from test_pyproject.foo import foo


def test_foo():
    assert foo("foo") == "foo"
