import pytest
import sys
from xmldt import XmlDt


def test_simple_file():
    class T1 (XmlDt):
        pass

    t1 = T1(strip=True, empty=False)
    assert t1(filename="tests/test1.xml") == """<root>text<body>more text<something value="2"/></body>text</root>"""


def test_simple_types():
    class T1 (XmlDt):
        _types = {"list": "list"}

        def list(self, e):
            assert type(e.c) is list
            assert len(e.c) == 3
            return e.c

        def item(self, e):
            return e.tag

        def tests(self, e):
            assert type(e.c) is list

    t1 = T1(strip=True, empty=False)
    t1(filename="tests/test2.xml")


def test_simple_types2():
    class T1 (XmlDt):
        _types = {"list": "list", "tests": "mmapwn", "submap" : "map"}

        def __default__(self, element):
            return element.c

        def list(self, e):
            assert type(e.c) is list
            assert len(e.c) == 3
            return e.c

        def submap(self, e):
            assert type(e.c) is dict
            assert "zbr" in e.c
            assert e.c["zbr"] == "Zbr"

        def tests(self, e):
            assert type(e.c) is dict
            assert len(e.c["aut"]) == 2
            assert len(e.c["list"]) == 3
            assert e.c["tit"] == "ttt"

        def item(self, e):
            return e.tag

    t1 = T1(strip=True, empty=False)
    t1(filename="tests/test4.xml")


def test_zero_type():
    class T1 (XmlDt):
        _types = {"list": "zero"}

        def __default__(self, e):
            return e.xml

    t1 = T1(strip=True, empty=False)
    assert t1(filename="tests/test2.xml") == "<tests/>"


def test_unknown_type():
    class T1 (XmlDt):
        _types = {"list": "junk"}

    t1 = T1(strip=True, empty=False)
    with pytest.raises(Exception):
        t1(filename="tests/test3.xml")
