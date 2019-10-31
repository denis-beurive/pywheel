import unittest
from my_package.my_module import hello_world


class TestMyModule(unittest.TestCase):

    def test_hello_world(self):
        self.assertEqual(hello_world(), "Hello World")

