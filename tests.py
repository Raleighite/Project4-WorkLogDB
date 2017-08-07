import unittest
from unittest import mock

from playhouse.test_utils import test_database
from peewee import *

import work_log

test_db = SqliteDatabase(':memory:')



class MenuTests(unittest.TestCase):
    @mock.patch('builtins.input', return_value='q')
    def test_main_menu(self, mock_input):
        self.assertRaises(SystemExit, work_log.display_menu())

if __name__ == '__main__':
    unittest.main()
