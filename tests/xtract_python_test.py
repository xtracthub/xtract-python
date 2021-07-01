import sys
import os
import unittest
from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.append(path)
import xtract_python_main as xpm

class xtract_python_main_tests(unittest.TestCase):
    def get_cwd(self):
        print("cwd: " + str(os.getcwd()))

    def get_imports_test(self):
        with open('expected/get_imports_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."
        with open('expected/get_imports_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."
        with open('expected/get_imports_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."

    def get_functions_test(self):
        with open('expected/get_functions_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."
        with open('expected/get_functions_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."
        with open('expected/get_functions_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('test_files/mixed_line.py')))
            assert expected == output, "mixed_line test failed."

    def extract_python_test(self):
        with open('expected/extract_python_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('test_files/single_line.py'))
            assert expected == output
        with open('expected/extract_python_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('test_files/multi_line.py'))
            assert expected == output
        with open('expected/extract_python_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.extract_python('test_files/mixed_line.py'))
            assert expected == output

    def python_len_test(self):
        assert xpm.python_len('test_files/single_line.py') == 22
        assert xpm.python_len('test_files/multi_line.py') == 43
        assert xpm.python_len('test_files/mixed_line.py') == 76

    def pep8_compliance_test(self):
        assert xpm.pep8_compliance('test_files/single_line.py') == (True, [])
        assert xpm.pep8_compliance('test_files/multi_line.py') == (True, [])
        assert xpm.pep8_compliance('test_files/mixed_line.py') == (True, [])
        with open('expected/pep8_compliance_test1.txt') as file:            
            expected = file.read()
            output = str(xpm.pep8_compliance('test_files/pep8_compliance_test1.py'))
            assert expected == output
    
    def num_calls_open_test(self):
        assert xpm.num_calls_open('test_files/num_calls_open_test1.py') == 13




test = xtract_python_main_tests()
test.get_imports_test()
test.get_functions_test()
test.extract_python_test()
test.python_len_test()
test.pep8_compliance_test()
test.num_calls_open_test()

# Seems to work
# xpm.get_compilation_version('test_files/single_line.py')

print(xpm.get_compatible_version('test_files/single_line.py'))
