import unittest
""" Module for testing console"""
from console import HBNBCommand
# from uuid import uuid4


class MyTestCase(unittest.TestCase):
    """ Class to test the console """
    def test_do_create_with_args(self):
        """ create a model """
        base_id = HBNBCommand.do_create(HBNBCommand.do_create, "BaseModel")
        self.assertEqual(base_id, None)  # add assertion here


if __name__ == '__main__':
    unittest.main()
