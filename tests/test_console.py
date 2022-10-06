import unittest
""" Module for testing console"""
from console import HBNBCommand
import os
import sys
import models
import unittest
from io import StringIO
from unittest.mock import create_autospec


class TestConsole(unittest.TestCase):
    """ Class to test the console """
    def setUp(self):
        """
        set up
        """
        self.backup = sys.stdout
        self.capt_out = StringIO()
        sys.stdout = self.capt_out

    def tearDown(self):
        """
        tear down
        """
        sys.stdout = self.backup


if __name__ == '__main__':
    unittest.main()
