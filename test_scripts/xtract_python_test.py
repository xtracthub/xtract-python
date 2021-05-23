import sys, os
import unittest
from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.append(path)

import xtract_python_main as xpm

class FunctionExtractionTests(unittest.TestCase):
    def single_line(self):
        with open('single_line_expected.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('single_line.py')))
            assert expected == output, "single_line test failed."

    def multi_line(self):
        with open('multi_line_expected.txt') as file:
            expected = file.read()
            output = str(xpm.get_functions(xpm.get_file_contents('multi_line.py')))
            assert expected == output, "multi_line test failed."


test_0 = FunctionExtractionTests()
test_0.single_line()
test_0.multi_line()
