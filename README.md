# makedoc

This is the makedoc project.

This repo aims to implement a command line tool to enable auto documentation file
generation. This would be used for generating beautiful `README.md` files !

For example, this README file and all the READMEs of this repo have been generated
this way !

## Installation

Just run the following command in your python virtual environment 

```
pip install git+https://github.com/JBocage/makedoc@dev
```

## Get started

To get an insight on all the possibilities this command line tool offers, you can run

```
makedoc
```

## Contribute

You please feel free to fork this repo.

If you wish to contribute, you can also email me at julien.bocage@gmail.com

<hr style="border:2px solid gray"> </hr>

# Structure

```
makedoc/
├── src/
│   └── makedoc/
│       ├── cli/
│       │   ├── commands/
│       │   │   ├── bash_scripts/
│       │   │   ├── __init__.py
│       │   │   ├── check.py
│       │   │   ├── config.py
│       │   │   ├── generate.py
│       │   │   ├── init.py
│       │   │   ├── pack.py
│       │   │   ├── unpack.py
│       │   │   └── update.py
│       │   ├── __init__.py
│       │   └── main.py
│       ├── logging/
│       │   ├── messages/
│       │   │   ├── concept/
│       │   │   │   └── message_abstract.py
│       │   │   ├── info.py
│       │   │   ├── success.py
│       │   │   └── warnings.py
│       │   └── logger.py
│       ├── parsers/
│       │   ├── concept/
│       │   │   ├── __init__.py
│       │   │   ├── file_parser_abstract.py
│       │   │   └── parser_abstract.py
│       │   ├── __init__.py
│       │   ├── directory_parser.py
│       │   ├── pyscript_parser.py
│       │   └── source_directory_parser.py
│       ├── utils/
│       │   └── config_dict_struc.py
│       ├── __init__.py
│       └── makedoc_paths.py
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
└── setup.py
```
<hr style="border:2px solid gray"> </hr>

## src
>
>This is the source directory. All the useful code should be contained there !

---

## setup.py
>The setup file for the project

---





<sub>This doc was automatically generated with makedoc v(0, 0, 2) on  09/30/22 18:46:03 