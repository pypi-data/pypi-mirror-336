xmldt - a Python module to process XML/HTML files in natural way

# Synopsis

    pydt file.xml > proc.py

    from xmldt import XmlDt
    

# pydt script

`pydt` is used to bootstrap the processing task

# `xmldt` variables and functions

    class proc(XmlDt):      # or class proc(HtmlDt) for HTML


    proc(strip=True,        # _flags dictionary
         empty=False,            # keep spaces
         ns_strip= ???

    proc(filename="x.xml")


- `__defaul__(s,ele)`
- `__pcdata__(s,text)`
- `__comment__(s,txt)`
- `__end__(s,result)`
- `__join__(s,ele)`

- `@XmlDt.dt_tag("id-id")\ndef id_id(s, e):.... `

## toxml function

```
    toxml("foo", {})                     == "<foo/>"
    toxml("foo", {"a": "b"})             == "<foo a=\"b\"/>"
    toxml("foo", {}, "bar")              == "<foo>bar</foo>"
    toxml("foo", {}, {"a": "b", "c": "d"}) == "<foo><a>b</a><c>d</c></foo>"
    toxml("foo", {}, ["a", "b"])         == "<foo>a</foo><foo>b</foo>"
    toxml("foo", {"a": "b"}, ["a", "b"]) == "<foo a=\"b\">a</foo><foo a=\"b\">b</foo>"
    toxml("foo", {}, ["a", "b"], ["c"])  == "<foo><item>a</item><item>b</item><item>c</item></foo>"

``` 

## Function Class Element

```
   ele = Element("tag", {"c":"d"}, "contents")
   ele.xml                      "<tag c='d'>contents</tag>"
   ele.toxml(v={"a":"b"})       "<tag a='b'>contents</tag>"
   ele.tag        ele.tag="val"            or ele.q
   ele.contents   ele.c = """.... """      or ele.c
   ele["att"]   : value or None            ele.attrs or ele.v
   
```

## element functions and methods

- ele.parent  : element or None
- ele.parent.tag : tag-name
- ele["root"]
- ele["gparent"]
- ele.in_context("tag1")
- ele._dt           

## (DT)self functions and methods (usefull for example, in `__pcdata__`)

- `s._path`     or s.dt_path
- `s._parent`   or s.dt_parent     = s._path[-1]
- `s._gparent`  or s.dt_gparent    = s._path[-2]
- `s._root`     or s.dt_root       = s._path[0]

# `types`

    _types = { 'table' : 'list', 'tr' : 'list', 'td' : 'list' }

Valid types are

- zero     -- return "" and skip processing subtree
- list     -- list of the subelement values
- map      -- map subelement-tags to their values
- mmap     -- map subelement-tags to the list of their values
- mmapwn   -- multimap when necessary (more than one ocor.)


##
