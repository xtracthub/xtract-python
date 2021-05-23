import sys, os
import unittest
from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.append(path)

import xtract_python_main as xpm

class xtract_python_main_tests(unittest.TestCase):
    def get_imports_test(self):
        with open('get_imports_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('single_line.py')))
            assert expected == output, "single_line test failed."

        with open('get_imports_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('multi_line.py')))
            assert expected == output, "multi_line test failed."
        
        with open('get_imports_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('single_line.py')))
            assert expected == output, "single_line test failed."

    def get_functions_test(self):
        with open('get_functions_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('single_line.py')))
            assert expected == output, "single_line test failed."
        
        with open('get_functions_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('multi_line.py')))
            assert expected == output, "multi_line test failed."

        with open('get_functions_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('mixed_line.py')))
            assert expected == output, "mixed_line test failed."

    def extract_python_test(self):
        with open('extract_python_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('single_line.py'))
            assert expected == output

        with open('extract_python_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('multi_line.py'))
            assert expected == output

        with open('extract_python_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('mixed_line.py'))
            assert expected == output

test = xtract_python_main_tests()
test.get_imports_test()
test.get_functions_test()
test.extract_python_test()

