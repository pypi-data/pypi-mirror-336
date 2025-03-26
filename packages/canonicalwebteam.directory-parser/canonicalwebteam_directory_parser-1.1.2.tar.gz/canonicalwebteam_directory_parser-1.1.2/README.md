# canonicalwebteam.directory-parser
Flask extension to parse websites and extract structured data to build sitemaps.

## Install
Install the project with pip: `pip install canonicalwebteam.directory-parser`

You can add the extension on your project by doing the following:

```
from canonicalwebteam.directory_parser import scan_directory

node = scan_directory("<example-templates-path>)
```

`node` will return a tree of all the templates given in the `<example-templates-path>

## Local development

### Linting and formatting

Tests can be run with Tox:
```
pip3 install tox  # Install tox
tox -e lint       # Check the format of Python code
tox -e format     # Reformat the Python code
```
