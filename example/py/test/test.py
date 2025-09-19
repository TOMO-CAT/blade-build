import unittest

from example.py.test import test_lib


class LibTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAdd(self):
        self.assertEqual(3, test_lib.add(1, 2))


if __name__ == "__main__":
    unittest.main()
