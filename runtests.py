import sys
import unittest
import doctest


def get_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("test_range")
    suite.addTest(doctest.DocTestSuite("nasuta"))
    suite.addTest(doctest.DocFileSuite('README.rst', optionflags=doctest.ELLIPSIS))

    return suite

def main():
    result = unittest.TestResult()
    get_suite().run(result)
    for error in result.errors:
        print(error)

if __name__ == '__main__':
    main()
