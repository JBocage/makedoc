# src

This is the source directory. All the useful code should be contained there !
<hr style="border:2px solid gray"> </hr>

# Structure

```
src/
├── makedoc/
│   ├── cli/
│   │   ├── commands/
│   │   │   ├── bash_scripts/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── generate.py
│   │   │   ├── init.py
│   │   │   ├── pack.py
│   │   │   ├── unpack.py
│   │   │   └── update.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── logging/
│   │   ├── messages/
│   │   │   ├── concept/
│   │   │   │   └── message_abstract.py
│   │   │   ├── info.py
│   │   │   ├── success.py
│   │   │   └── warnings.py
│   │   └── logger.py
│   ├── parsers/
│   │   ├── concept/
│   │   │   ├── __init__.py
│   │   │   ├── file_parser_abstract.py
│   │   │   └── parser_abstract.py
│   │   ├── __init__.py
│   │   ├── directory_parser.py
│   │   ├── pyscript_parser.py
│   │   └── source_directory_parser.py
│   ├── utils/
│   │   └── config_dict_struc.py
│   ├── __init__.py
│   └── makedoc_paths.py
└── makedoc.egg-info/
```
<hr style="border:2px solid gray"> </hr>

## makedoc
>
>Contains the code of the makedoc package.

---

## makedoc.egg-info
>

---





<sub>This doc was automatically generated with makedoc v(0, 0, 1) on  09/30/22 17:31:58 