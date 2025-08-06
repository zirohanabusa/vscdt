def test_hello() -> None:
    imported = False
    try:
        import example

        imported = True
    except BaseException:
        pass
    assert imported is True
    assert example.text() == "hello python world!"
