import re
import subprocess
import sys
import os
import pathlib
import json

EXTENSIONS = ['.py', '.py3']

def get_file_paths(dir_path=None):
    """Retrieves paths to python files in a given directory.

    Parameter:
    dir_path (str): Path of directory to get python file paths from.

    Return:
    python_paths (list): List of strings of python paths
    """
    if not dir_path or not os.path.isdir(dir_path):
        dir_path = str(os.getcwd())
        
    file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) 
    if os.path.isfile(os.path.join(dir_path, f)) and os.path.join(dir_path, f).endswith(tuple(EXTENSIONS))]

    return file_paths


def run_extractors(dir_path=None):
    """
    Run extractors on a list of python files.
    """

    all_extractors = lambda file_path, file_contents: dict({'comments' : get_comments(file_contents),
                                                            'imports' : get_imports(file_contents),
                                                            'functions' : get_functions(file_contents),
                                                            'num_lines' : python_len(file_path),
                                                            'num_open' : num_calls_open(file_path),
                                                            'pep8_compliance' : pep8_compliance(file_path),
                                                            'min_compatible_version' : get_min_compatible_version(file_path)})

    bundled_metadata = dict()
    file_paths = get_file_paths(dir_path)

    for file_path in file_paths:
        bundled_metadata[file_path] = all_extractors(file_path, get_file_contents(file_path))

    return bundled_metadata


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


def extract_python(file_path):
    """Retrieves basic metadata from python file.

    Parameter:
    file_path (str): Path of python file to retrieve metadata from.

    Return:
    metadata (dict): Imports and function info. from python file in the format
    {imports: {}, functions: {}}.
    """
    file_contents = get_file_contents(file_path)
    metadata = {}

    metadata["imports"] = get_imports(file_contents)
    metadata["functions"] = get_functions(file_contents)

    return metadata


def python_len(file_path):
    """Returns the number of lines in a python file.

    Parameter:
    file_path (str): Path of python file to determine number of lines.

    Return:
    length (int): number of lines in a python file.
    """
    file_contents = get_file_contents(file_path)
    length = 0

    for i in file_contents:
        if i == '\n':
            length += 1

    return length


def num_calls_arbitrary(file_path, function):
    """Returns the number of calls to arbitrary function made by a python
    file.

    Parameter(s):
    file_path (str): Path of python file to count number of calls to an
    arbitrary function.
    function (str): Name of the function to count number of calls to.

    Return:
    num_calls (int): number of calls made to a specific function.
    """
    file_contents = get_file_contents(file_path)
    pattern = r'(["\'])\1\1.*?' + function + \
        r'\(.*?\).*?\1{3}|#.*?' + function + r'\(.*?\).*?'
    stripped_file_contents = re.sub(
        pattern, '', file_contents, flags=re.DOTALL)

    num_calls = 0
    for _ in re.findall(function + r'\(.*?\)', stripped_file_contents):
        num_calls += 1

    return num_calls


def num_calls_open(file_path):
    """Returns the number of calls to the open function made by a python
    file.

    Parameter(s):
    file_path (str): Path of python file to count number of calls to the
    open function/system call.

    Return:
    num_calls (int): number of calls made to a specific function.
    """
    return num_calls_arbitrary(file_path=file_path, function='open')


def pep8_compliance(file_path):
    """Returns whether a python file meets PEP8 standards.

    Parameter:
    file_path (str): Path of python file to determine PEP8 compliance.

    Return:
    pep8 compliance (boolean): True if PEP8 compliant, False otherwise.
    """
    issues = []

    try:
        process = subprocess.run(
            ['pycodestyle', file_path], capture_output=True, text=True)
        for _, line, char, descrip in re.findall("(.*):(.*):(.*): (.*)", process.stdout):
            issue = {"line": line, "char": char, "description": descrip}
            issues.append(issue)
    except:
        print('Error: unable to run pycodestyle as subprocess.')
        return

    return len(process.stdout) == 0, issues


def get_min_compatible_version(file_path):
    """ Returns minimum compatible python version for a given file_path file.
    This is done by checking for features added throughout the different
    versions of python via the Vermin module. The output of calling the Vermin
    module is regex'd and returned as a list containing a dictionary for each
    python file in the directory.

    Parameter(s):
    file_path (str): Path of python file to determine compatible interpreter
    versions. file_path may either be a python file or a directory containing
    python files; currently only scripts ending in .py or .py3 are supported.

    Return:
    str: a minimum python version that works.
    """
    version_dict = []

    if os.path.isdir(file_path):
        # Should probably change this for something easier to read....
        file_paths = [os.path.join(file_path, f) for f in os.listdir(file_path) 
        if os.path.isfile(os.path.join(file_path, f)) and os.path.join(file_path, f).endswith('.py')]
        print(file_paths)
    else:
        file_paths = [file_path]

    try:
        for file_path in file_paths:
            process = subprocess.run(['vermin', '--format parsable', '-vvvv', file_path], capture_output=True, text=True)
        
            tmp_dict = {}
            details = []

            for py2, py3, path in re.findall(f'^([~!?0-9.]*), ([~!?0-9.]*)\s*(.*)$', process.stdout, flags=re.M):
                tmp_dict = {
                    'path': path,
                    'min_py2': py2,
                    'min_py3': py3
                }
        
            for loc, key, py2, py3 in re.findall(f'^  (L.*): (.*) requires (.*), (.*)$', process.stdout, flags=re.M):
                issue = {
                    'location': loc,
                    'keyword': key,
                    'py2_implemented': py2,
                    'py3_implemented': py3
                }
                details.append(issue)
                
            tmp_dict['details'] = details
            version_dict.append(tmp_dict)
        return version_dict
    except:
        print('Error: unable to run Vermin as subprocess.')
        return