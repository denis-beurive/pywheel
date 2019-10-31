# This file illustrates the use of the module "unittest".
#
# Usage:
#
#          python run_unittest.py

import os
from unittest import defaultTestLoader, TestSuite, TestResult, TestCase
from xmlrunner import xmlrunner
from tempfile import gettempdir


def main():

    __DIR__ = os.path.dirname(os.path.abspath(__file__))
    USE_XML_RUNNER = True

    # target: path to the directory used to store the generated XML files.
    # terminal_path: path to the file used to store the standard output of the
    #                test execution.

    top_directory = os.path.join(__DIR__, 'test', 'my_package')
    target = os.path.join(gettempdir(), 'result')
    terminal_path = os.path.join(gettempdir(), 'terminal')

    print(f'XML files will be generated under the directory "{target}".')
    print(f'Path to the terminal file: "{terminal_path}".')


    with open(terminal_path, 'w') as terminal:
        test_suite: TestSuite = defaultTestLoader.discover(start_dir=f'{top_directory}',
                                                           top_level_dir=__DIR__,
                                                           pattern='*_test.py')
        print(f'Number of unit tests: {test_suite.countTestCases()}')

        if USE_XML_RUNNER:
            test_result = xmlrunner.XMLTestRunner(output=target,
                                                  verbosity=0,
                                                  stream=terminal).run(test_suite)
        else:
            result = TestResult()
            test_suite.run(result)
            test_case: TestCase
            message: str
            for test_case, message in result.failures:
                print(test_case.id() + ':')
                print('\n'.join([f'\t{m}' for m in message.split('\n')]))


if __name__ == '__main__':
    main()
