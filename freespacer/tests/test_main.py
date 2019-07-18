import unittest
from somecommand.main import helloworld, main

class TestMain(unittest.TestCase):

    def test_helloworld(self):
        helloworld()
        self.assertTrue(True)
