# makedoc

<hr style="border:2px solid gray"> </hr>

# Structure

```
makedoc/
├── cli/
│   ├── commands/
│   │   ├── bash_scripts/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── generate.py
│   │   ├── init.py
│   │   ├── pack.py
│   │   ├── unpack.py
│   │   └── update.py
│   ├── __init__.py
│   └── main.py
├── parsers/
│   ├── concept/
│   │   ├── __init__.py
│   │   ├── file_parser_abstract.py
│   │   └── parser_abstract.py
│   ├── __init__.py
│   ├── directory_parser.py
│   ├── pyscript_parser.py
│   └── source_directory_parser.py
└── __init__.py
```
<hr style="border:2px solid gray"> </hr>

## cli
>
>This is the `cli` directory. It contains all the command line related code.

---

## parsers
>
>This is the `parsers` directory. It contains the code that implements various parser
>classes for walking through the directory files and parsing docs.

---





<sub>This doc was automatically generated with makedoc v(0, 0, 1) on  08/08/22 20:29:12 