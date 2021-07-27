import xtract_python_test as xpt

test = xpt.xtract_python_main_tests()
test.get_file_paths_test()
test.run_extractors_file_test()
test.run_extractors_dir_test()
test.get_file_contents_test()
test.get_comments_test()
test.get_imports_test()
test.get_functions_test()
test.extract_python_test()
test.python_len_test()
test.pep8_compliance_test()
test.num_calls_open_test()