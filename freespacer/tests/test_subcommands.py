import unittest
from somecommand.subcommands import foo, bar

class TestFooBar(unittest.TestCase):

    def test_foo(self):
        foo()
        self.assertTrue(True)

    def test_bar(self):
        bar()
        self.assertTrue(True)
