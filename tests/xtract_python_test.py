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
        with open('expected/pep8_compliance_noncompliant.txt') as file:
            expected = file.read()
            output = xpm.pep8_compliance('test_files/pep8_noncompliant_test.py')
            assert expected == output
    
    # def num_open_calls_test(self):




test = xtract_python_main_tests()
test.get_imports_test()
test.get_functions_test()
test.extract_python_test()
test.python_len_test()
test.pep8_compliance_test



# Preliminary test for get_comments function
# b = xpm.get_comments(xpm.get_file_contents('test_files/num_open_calls_test.py'))
# print(b)
# c = xpm.get_comments(xpm.get_file_contents('test_files/num_open_calls_test2.py'))
# print(c)

# d = xpm.num_open_calls('test_files/num_open_calls_test.py')
# print(d)

e = xpm.num_calls_arbitrary('test_files/num_open_calls_test.py', 'print')
print(e)
