import sys, os
import unittest
from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.append(path)

import xtract_python_main as xpm

class xtract_python_main_tests(unittest.TestCase):
    def get_cwd(self):
        print("cwd: " + str(os.getcwd()))

    def get_imports_test(self):
        with open('tests/expected/get_imports_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('tests/test_files/single_line.py')))
            assert expected == output, "single_line test failed."

        with open('tests/expected/get_imports_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('tests/test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."
        
        with open('tests/expected/get_imports_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('tests/test_files/single_line.py')))
            assert expected == output, "single_line test failed."

    def get_functions_test(self):
        with open('tests/expected/get_functions_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('tests/test_files/single_line.py')))
            assert expected == output, "single_line test failed."
        
        with open('tests/expected/get_functions_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('tests/test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."

        with open('tests/expected/get_functions_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('tests/test_files/mixed_line.py')))
            assert expected == output, "mixed_line test failed."

    def extract_python_test(self):
        with open('tests/expected/extract_python_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('tests/test_files/single_line.py'))
            assert expected == output

        with open('tests/expected/extract_python_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('tests/test_files/multi_line.py'))
            assert expected == output

        with open('tests/expected/extract_python_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('tests/test_files/mixed_line.py'))
            assert expected == output

test = xtract_python_main_tests()
test.get_imports_test()
# test.get_functions_test()
# test.extract_python_test()
# test.get_cwd()