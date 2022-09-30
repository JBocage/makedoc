# makedoc

Contains the code of the makedoc package.
<hr style="border:2px solid gray"> </hr>

# Structure

```
makedoc/
├── cli/
│   ├── commands/
│   │   ├── bash_scripts/
│   │   ├── __init__.py
│   │   ├── check.py
│   │   ├── config.py
│   │   ├── generate.py
│   │   ├── init.py
│   │   ├── pack.py
│   │   ├── unpack.py
│   │   └── update.py
│   ├── __init__.py
│   └── main.py
├── logging/
│   ├── messages/
│   │   ├── concept/
│   │   │   └── message_abstract.py
│   │   ├── info.py
│   │   ├── success.py
│   │   └── warnings.py
│   └── logger.py
├── parsers/
│   ├── concept/
│   │   ├── __init__.py
│   │   ├── file_parser_abstract.py
│   │   └── parser_abstract.py
│   ├── __init__.py
│   ├── directory_parser.py
│   ├── pyscript_parser.py
│   └── source_directory_parser.py
├── utils/
│   └── config_dict_struc.py
├── __init__.py
└── makedoc_paths.py
```
<hr style="border:2px solid gray"> </hr>

## cli
>
>This is the `cli` directory. It contains all the command line related code.

---

## logging
>
>The `logging` directory contains all the code relative to logging

---

## parsers
>
>This is the `parsers` directory. It contains the code that implements various parser
>classes for walking through the directory files and parsing docs.

---

## utils
>
>Contains utils functions for the project.
>
>This includes a typed dict definition for helping IDE autocompletion when writing code.

---

## __init__.py
>

---

## makedoc_paths.py
>Contains all the paths used by the package.
>
>
>
>    Attributes:
>
>        logs (pathlib.Path)
>
>            The path to .makedoc/logs/  # TODO: Implement logging
>
>        config (pathlib.Path)
>
>            The path to .makedoc/config/
>
>        packed_doc (pathlib.Path)
>
>            The path to the packed doc file.
>
>            .makedoc/packed_doc.json
>
>        ignored_path (pathlib.Path)
>
>            The path to the ignored paths file.
>
>            .makedoc/config/makedoc.ignored_paths
>
>        ignore_every (pathlib.Path)
>
>            The path to the ignore_every file.
>
>            .makedoc/config/makedoc.ignore_every
>
>        ignored_extensions (pathlib.Path)
>
>            The path to the ignored_extensions file.
>
>            .makedoc/config/makedoc.ignored_extensions
>
>        files_naming (pathlib.Path)
>
>            The path to the files naming file.
>
>            .makedoc/config/makedoc.files_naming.json
>
>
>
>    Properties:
>
>        unpacked_doc_file_name (str)
>
>            The file name of the directory unpacked doc
>
>        autodoc_file_name (str)
>
>            The file name of the doc md files (default: README.md)

---





<sub>This doc was automatically generated with makedoc v(0, 0, 2) on  09/30/22 18:46:03 