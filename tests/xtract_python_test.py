import sys
import os
import unittest
from pathlib import Path

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.append(path)

import xtract_python_main as xpm

class xtract_python_main_tests(unittest.TestCase):
    @staticmethod
    def get_cwd():
        return f'cwd: {str(os.getcwd())}'

    def get_file_paths_test(self):
        with open('expected/get_file_paths_test_files.txt') as file:
            expected = file.read()
            output = str(xpm.get_file_paths('test_files/'))
            assert expected == output, "test_files directory failed."
        with open('expected/get_file_paths_tests.txt') as file:
            expected = file.read()
            output = str(xpm.get_file_paths('../tests'))
            assert expected == output, "tests directory failed."

    def run_extractors_file_test(self):
        pass

    def run_extractors_dir_test(self):
        pass

    def get_file_contents_test(self):
        with open('expected/get_file_contents_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_file_contents('test_files/single_line.py'))
            assert expected == output, "single_line test failed."
        with open('expected/get_file_contents_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_file_contents('test_files/multi_line.py'))
            assert expected == output, "multi_line test failed."
        with open('expected/get_file_contents_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_file_contents('test_files/mixed_line.py'))
            assert expected == output, "mixed_line test failed."

    def get_comments_test(self):
        with open('expected/get_comments_single_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/single_line.py')
            output = str(xpm.get_comments(file_contents))
            assert expected == output, "single_line test failed."
        with open('expected/get_comments_multi_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/multi_line.py')
            output = str(xpm.get_comments(file_contents))
            assert expected == output, "multi_line test failed."
        with open('expected/get_comments_mixed_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/mixed_line.py')
            output = str(xpm.get_comments(file_contents))
            assert expected == output, "mixed_line test failed."
        
    def get_imports_test(self):
        with open('expected/get_imports_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(
                xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."
        with open('expected/get_imports_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(
                xpm.get_file_contents('test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."
        with open('expected/get_imports_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_imports(
                xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."

    def get_functions_test(self):
        with open('expected/get_functions_single_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(
                xpm.get_file_contents('test_files/single_line.py')))
            assert expected == output, "single_line test failed."
        with open('expected/get_functions_multi_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(
                xpm.get_file_contents('test_files/multi_line.py')))
            assert expected == output, "multi_line test failed."
        with open('expected/get_functions_mixed_line.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(
                xpm.get_file_contents('test_files/mixed_line.py')))
            assert expected == output, "mixed_line test failed."

    def extract_python_test(self):
        with open('expected/extract_python_single_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/single_line.py')
            output = str(xpm.extract_python(file_contents))
            assert expected == output
        with open('expected/extract_python_multi_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/multi_line.py')
            output = str(xpm.extract_python(file_contents))
            assert expected == output
        with open('expected/extract_python_mixed_line.txt') as file:
            expected = file.read()
            file_contents = xpm.get_file_contents('test_files/mixed_line.py')
            output = str(xpm.extract_python(file_contents))
            assert expected == output

    def python_len_test(self):
        file_contents = xpm.get_file_contents('test_files/single_line.py')
        assert xpm.python_len(file_contents) == 22
        file_contents = xpm.get_file_contents('test_files/multi_line.py')
        assert xpm.python_len(file_contents) == 43
        file_contents = xpm.get_file_contents('test_files/mixed_line.py')
        assert xpm.python_len(file_contents) == 76

    def pep8_compliance_test(self):
        assert xpm.pep8_compliance('test_files/single_line.py') == (True, [])
        assert xpm.pep8_compliance('test_files/multi_line.py') == (True, [])
        assert xpm.pep8_compliance('test_files/mixed_line.py') == (True, [])
        with open('expected/pep8_compliance_test1.txt') as file:
            expected = file.read()
            output = str(xpm.pep8_compliance(
                'test_files/pep8_compliance_test1.py'))
            assert expected == output

    def num_calls_open_test(self):
        file_contents = xpm.get_file_contents('test_files/num_calls_open_test1.py')
        assert xpm.num_calls_open(file_contents) == 13
    
    def get_min_compatible_version_test(self):
        """
        Testing methodology: test files will consist of features added to Python
        in the major revisions, referenced from the 'What's New in Python' page
        from the official documentation.
        """
        with open('expected/get_min_compatible_version_test1.txt') as file:
            expected = file.read(
