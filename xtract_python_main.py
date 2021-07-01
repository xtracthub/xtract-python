import re
import subprocess
import sys
import os

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

def get_comments(file_contents):
    """Retrieves comments in a python file. Note that technically multi-line
    strings are not 'comments' per PEP8, but they will be considered as such
    for the purposes of this extractor.

    Parameter:
    file_contents (str): Contents of python file.

    Return:
    comments (arr): an array of comments
    """
    comments = []

    for quote, comment in re.findall(r'([\'"])\1\1(.*?)\1{3}', file_contents, re.DOTALL):
        comments.append(comment.strip())
    
    for comment in re.findall(r'#(.*)', file_contents):
        comments.append(comment.strip())

    return comments


def get_imports(file_contents):
    """Retrieves imported libraries and functions.

    Parameter:
    file_contents (str): Contents of python file.

    Return:
    imports (dict): Imported libraries and functions in the format
    {library: [imported_functions]}.
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
        functions[function] = {"params": re.split(
            ",", parameters), "docstring": ""}

    for function, parameters, docstring in re.findall("def (.*)\((.*)\):\n\s*\"{3}(.*)\"{3}", file_contents):
        functions[function] = {"params": re.split(
            ",", parameters), "docstring": docstring}

    for function, parameters, docstring in re.findall('def (.*?)\((.*?)\):\s*\"{3}(.*?)\"{3}', file_contents, flags=re.DOTALL):
        functions[function] = {"params": re.split(
            ",", parameters), "docstring": re.sub('\s+', " ", docstring.strip())}

    return functions


def extract_python(python_path):
    """Retrieves basic metadata from python file.

    Parameter:
    python_path (str): Path of python file to retrieve metadata from.

    Return:
    metadata (dict): Imports and function info. from python file in the format
    {imports: {}, functions: {}}.
    """
    file_contents = get_file_contents(python_path)
    metadata = {}

    metadata["imports"] = get_imports(file_contents)
    metadata["functions"] = get_functions(file_contents)

    return metadata


def python_len(python_path):
    """Returns the number of lines in a python file.

    Parameter:
    python_path (str): Path of python file to determine number of lines.

    Return:
    length (int): number of lines in a python file.
    """
    file_contents = get_file_contents(python_path)
    length = 0

    for i in file_contents:
        if i == '\n':
            length += 1

    return length

def pep8_compliance(python_path):
    """Returns whether a python file meets PEP8 standards.

    Parameter:
    python_path (str): Path of python file to determine PEP8 compliance.

    Return:
    pep8 compliance (boolean): True if PEP8 compliant, False otherwise.
    """
    issues = []

    try:
        process = subprocess.run(['pycodestyle', python_path], capture_output=True, text=True)
        for _, line, char, descrip in re.findall("(.*):(.*):(.*): (.*)", process.stdout):
            issue = {"line": line, "char": char, "description": descrip}
            issues.append(issue)
    except:
        print('Error: unable to run pycodestyle as subprocess.')
        return

    return len(process.stdout) == 0, issues

def num_calls_arbitrary(python_path, function):
    """Returns the number of calls to arbitrary function made by a python
    file.

    Parameter(s):
    python_path (str): Path of python file to count number of calls to an
    arbitrary function.
    function (str): Name of the function to count number of calls to.

    Return:
    num_calls (int): number of calls made to a specific function.
    """
    file_contents = get_file_contents(python_path)
    pattern = r'(["\'])\1\1.*?' + function + r'\(.*?\).*?\1{3}|#.*?' + function + r'\(.*?\).*?'
    stripped_file_contents = re.sub(pattern, '', file_contents, flags=re.DOTALL)

    num_calls = 0
    for _ in re.findall(function + r'\(.*?\)', stripped_file_contents):
        num_calls += 1
    
    return num_calls

def num_calls_open(python_path):
    """Returns the number of calls to the open function made by a python
    file.

    Parameter(s):
    python_path (str): Path of python file to count number of calls to the
    open function/system call.

    Return:
    num_calls (int): number of calls made to a specific function.
    """
    return num_calls_arbitrary(python_path=python_path, function='open')

def get_compilation_version(python_path):
    """Returns the version of the python interpreter used when executing
    a python script.

    Parameter(s):
    python_path (str): Path of python file to get version of intepreter used.

    Return:
    version[0] (str): Version of python interpreter as a string.
    """
    inject = 'import platform\nprint(platform.python_version())\n\n'
    old_script = get_file_contents(python_path)
    new_script = inject + old_script

    new_path = os.path.splitext(python_path)[0] + '_inj.py'

    with open(new_path, 'w') as f:
        f.write(new_script)

    process = subprocess.run(['python', new_path], capture_output=True, text=True)
    os.remove(new_path)

    output = process.stdout
    version = re.search('(.*?)$', output)

    return version[0]


def get_compatible_version(python_path):
    """Returns compatible versions of python with a given python script.

    Parameter(s):
    python_path (str): Path of python file to determine compatible interpreter
    versions.

    Return:
    (bool, bool): A tuple returning the compability of the python script with
    the python2 interpreter and the python3 interpreter, respectively.
    """
    py2_proc = subprocess.run(['python2', python_path], capture_output=True, text=True)
    py3_proc = subprocess.run(['python3', python_path], capture_output=True, text=True)
    
    return len(py2_proc.stderr) == 0, len(py3_proc.stderr) == 0
