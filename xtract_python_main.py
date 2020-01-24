import re


def get_file_contents(file_path):
    """Retrieves contents from a file.

    Parameter:
    file_path (str): Path of file to get contents from.

    Return:
    file_contents (str): Contents from file_path.
    """
    with open(file_path) as f:
        file_contents = f.read()

    return file_contents


def get_imports(file_contents):
    """Retrieves imported libraries and functions.

    Parameter:
    file_contents (str): Contents of python file.

    Return:
    imports (dict): Imported libraries and functions in the format {library: [imported_functions]}.
    """
    imports = {}

    for library in re.findall("^import (.*)", file_contents, re.M):
        imports.update({library: []})

    for library, functions in re.findall("^from (.*) import (.*)", file_contents, re.M):
        imports.update({library: re.split(",", functions)})

    return imports


def get_functions(file_contents):
    """Returns information about functions.

    Parameter:
    file_contents (str): Contents of python file.

    Return:
    functions (dict): Function name, parameters, docstring in the format
    {function: {parameters: [params], docstring: docstring}}
    """
    functions = {}

    for function, parameters in re.findall("def (.*)\((.*)\)", file_contents):
        functions[function] = {"params": re.split(",", parameters), "docstring": ""}

    for function, parameters, docstring in re.findall("def (.*)\((.*)\):\n\s*\"{3}(.*)\"{3}", file_contents):
        functions[function] = {"params": re.split(",", parameters), "docstring": docstring}

    return functions


def extract_python(python_path):
    """Retrieves basic metadata from python file.

    Parameter:
    python_path (str): Path of python file to retrieve metadata from.

    Return:
    metadata (dict): Imports and function info. from python file in the format {imports: {}, functions: {}}.
    """
    file_contents = get_file_contents(python_path)
    metadata = {}

    metadata["imports"] = get_imports(file_contents)
    metadata["functions"] = get_functions(file_contents)

    return metadata
