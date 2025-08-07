html: str = """
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>てすと</title>     
</head>
<body>
    <header>
    </header>
    <main>
         <ul>
            <li>aaaaa </li>
            <li>bbbb</li>
            <li>ccc</li>
            <li>dd</li>
            <li>e</li>
         </ul>
    </main>
    <footer>
    </footer>
</body>
</html>
"""

json: str = """
{
  "int": 1,
  "float": 3.141,
  "bool": true,
  "string": "hoge",
  "null": null,
  "array": [
    2,
    2.718,
    false,
    "foo",
    null,
    [],
    {}
  ],
  "object": {
    "int": 3,
    "float": 0.5772,
    "bool": true,
    "string": "bar",
    "null": null,
    "array": [],
    "object": {}
  }
}
"""


def test_import_crawl_selector_module() -> None:
    imported: bool = False
    try:
        from crawl.selector import HtmlNode, HtmlNodes, JsonNode, JsonNodes

        imported = True
    except BaseException:
        pass
    assert imported is True


def test_html_select() -> None:
    from crawl.selector import HtmlNode

    parsed: bool = False
    try:
        root = HtmlNode.from_string(html)
        parsed = True
    except BaseException:
        pass
    assert parsed is True

    li_list = root.xpath("//li")
    assert len(li_list) == 5

    li_get_all = li_list.get_all()
    assert li_list[0].get() == "<li>aaaaa </li>"
    assert li_list[1].get() == "<li>bbbb</li>"
    assert li_list[2].get() == "<li>ccc</li>"
    assert li_list[3].get() == "<li>dd</li>"
    assert li_get_all[4] == "<li>e</li>"

    li_get_text_all = li_list.get_text_all()
    assert li_get_text_all[0] == "aaaaa "
    assert li_list[1].get_text() == "bbbb"
    assert li_list[2].get_text() == "ccc"
    assert li_list[3].get_text() == "dd"
    assert li_list[4].get_text() == "e"


def test_json_select() -> None:
    from crawl.selector import JsonNode

    root = JsonNode.from_string(json)
    # jsonpath
    assert root.jsonpath("$.int").get() == 1
    assert root.jsonpath("$.float").get() == 3.141
    assert root.jsonpath("$.bool").get() is True
    assert root.jsonpath("$.string").get() == "hoge"
    assert root.jsonpath("$.null").get() is None
    assert root.jsonpath("$.array[2]").get() is False
    assert root.jsonpath("$.object.string").get() == "bar"
    # jmespath
    assert root.jmespath("string").get() == "hoge"
    assert root.jmespath("array[3]").get() == "foo"
    assert root.jmespath("object.string").get() == "bar"
