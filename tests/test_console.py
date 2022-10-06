import unittest
""" Module for testing console"""
from console import HBNBCommand
import os
import sys
import models
import unittest
from io import StringIO
from unittest.mock import create_autospec, patch
from uuid import UUID


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

    def create(self):
        """
        create an instance of HBNBCommand class
        """
        return HBNBCommand()

    # def test_quit(self):
    #     """ Test quit exists """
    #     console = self.create()
    #     # console.onecmd("quit")
    #     # self.assertTrue(console.onecmd("quit"))
    #     console.onecmd("quit")
    #     self.assertTrue(self.capt_out.getvalue(), None)

    # def test_EOF(self):
    #     """ Test EOF exists """
    #     console = self.create()
    #     self.assertTrue(console.onecmd("EOF"))
    #     self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    def test_all(self):
        """ test for all """
        console = self.create()
        console.onecmd("all")
        self.assertTrue(isinstance(self.capt_out.getvalue(), str))

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "This wont work for db storage"
    )
    def test_show(self):
        """
        test for show
        """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        # break output and do onecmd
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        # continue
        console.onecmd("show User " + user_id)
        out = self.capt_out.getvalue()
        self.assertTrue(isinstance(out, str))

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "This wont work for db storage"
    )
    def test_show_missing_classname(self):
        """
        test for show missing class name
        """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        # break output and do onecmd
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        # continue
        console.onecmd("show")
        out = self.capt_out.getvalue()
        self.assertEqual("** class name missing **\n", out)

    def test_show_missing_id(self):
        """
        test for show missing instance id
        """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        # break output and do onecmd
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        # continue
        console.onecmd("show User")
        out = self.capt_out.getvalue()
        self.assertEqual("** instance id missing **\n", out)

    def test_show_no_instance(self):
        """
        test for show no instance
        """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        # break output and do onecmd
        sys.stdout = self.backup
        self.capt_out.close()
        self.capt_out = StringIO()
        sys.stdout = self.capt_out
        # continue
        console.onecmd("show User 1234")
        out = self.capt_out.getvalue()
        self.assertEqual("** no instance found **\n", out)

    def test_create_file_storage(self):
        """
        test for create instance
        """
        console = self.create()
        console.onecmd("create User")
        user_id = self.capt_out.getvalue()
        self.assertTrue(isinstance(user_id, str))

    def test_create_class_missing(self):
        """
        test for create instance with missing class
        """
        console = self.create()
        console.onecmd("create")
        out = self.capt_out.getvalue()
        self.assertEqual('** class name missing **\n', out)

    def test_create_class_not_exist(self):
        """
        test for create instance with invalid class
        """
        console = self.create()
        console.onecmd("create Manuel")
        out = self.capt_out.getvalue()
        self.assertEqual("** class doesn't exist **\n", out)

# with patch('sys.stdout', new=StringIO()) as f:
#     HBNBCommand.onecmd("help show")


if __name__ == '__main__':
    unittest.main()
