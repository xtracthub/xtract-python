
# xtract-python

## Functionality (WIP)

Currently supported functionality as of 07/01/2021. Documentation is provided as WIP.

|Method              |Description 
|:-------------------|:------------------------------|
|get_file_contents|Returns entirety of python script as a string.
|get_comments|Returns a dictionary of commented sections of a python script.
|get_imports|Returns a dictionary of module imports in a python script.
|get_functions|Returns a dictionary of functions in a python script; a function entry is comprised of its name, parameters, and docstring if present.
|extract_python|Retrieves functions and imports.
|python_len|Retrieves the number of lines in a python script.
|pep8_compliance|Returns PEP8 compliance of a python script, along with an array of issues found, if any.
|num_calls_arbitrary|Returns the number of calls made to any arbitrary function.
|num_calls_open|Returns the number of calls made to the open() syscall.
|get_compilation_version|Returns the version that a python script is interpreted with at runtime.
|get_compatible_version|Returns a tuple of versions of python interpreters that are compatible with a given python script.

## To-Do
 - [ ] Add types for input parameters and return variables to function extraction.
 - [ ] Add return to function extraction. We include the input parameters, so why not the return parameter?
 - [ ] Find a way to test get_compilation_version and get_compatible_version. Perhaps this could be achieved by finding features that were implemented in each major version of 2.X and 3.X and ensuring that the the interpreter version is as expected.
 - [ ] Perhaps some structure that gives a quick summary of the metadata extracted? This could take the form of a dictionary.
