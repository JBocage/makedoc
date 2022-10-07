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
>

---

## pyscript_parser.py
>Implements a parser class for python scripts
>
>
>
>```python
>    def get_dynamic_snippet_processed_file_docstrings(self) -> List[str]:
>        docstrings = self.get_file_beginning_comment_lines()
>        dynamic_snippets = self.get_dynamic_snippets()
>
>        processed_lines = []
>        for line in docstrings:
>            tokens = re.search(r"makedoc-snippet:([\w\-_]+)", line)
>            if tokens:
>                snip_name = tokens.groups()[0]
>                if snip_name not in dynamic_snippets.keys():
>                    self.logger.add_log(
>                        UnreferencedDynamicSnippetWarning(*self._message_args)
>                    )
>                else:
>                    # processed_lines.extend(
>                    #     ["> " + l + "\n>" for l in dynamic_snippets[snip_name]]
>                    # )
>                    processed_lines.append("```python")
>                    processed_lines.extend(dynamic_snippets[snip_name])
>                    processed_lines.append("```")
>            else:
>                processed_lines.append(line + "\n")
>
>        return processed_lines
>```

---

## source_directory_parser.py
>> author: Julien Bocage
>
>> author-email: julien.bocage@gmail.com
>
>
>
>Implements a parser class for the source directory of a project
>

---





<sub>This doc was automatically generated with makedoc v(0, 0, 2) on  10/04/22 15:24:35 