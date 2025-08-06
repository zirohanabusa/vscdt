def test_hello() -> None:
    imported = False
    try:
        import crawl

        imported = True
    except BaseException:
        pass
    assert imported is True
    assert crawl.text() == "hello python world!"
