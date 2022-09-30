# parsers

This is the `parsers` directory. It contains the code that implements various parser
classes for walking through the directory files and parsing docs.
<hr style="border:2px solid gray"> </hr>

# Structure

```
parsers/
├── concept/
│   ├── __init__.py
│   ├── file_parser_abstract.py
│   └── parser_abstract.py
├── __init__.py
├── directory_parser.py
├── pyscript_parser.py
└── source_directory_parser.py
```
<hr style="border:2px solid gray"> </hr>

## concept
>
>The `concept` directory should contain all abstract and base classes for the parsers
>implemented outside.

---

## __init__.py
>

---

## directory_parser.py
>Implements a parser class for directories

---

## pyscript_parser.py
>Implements a parser class for python scripts

---

## source_directory_parser.py
>> author: Julien Bocage
>
>> author-email: julien.bocage@gmail.com
>
>
>
>Implements a parser class for the source directory of a project

---





<sub>This doc was automatically generated with makedoc v(0, 0, 1) on  09/30/22 17:31:58 