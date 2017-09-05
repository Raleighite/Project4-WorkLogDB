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

    @mock.patch('work_log.new_entry')
    def test_menu_called_new(self, add_mock):
        with mock.patch('builtins.input', return_value='n'):
            self.assertTrue(work_log.new_entry)

    @mock.patch('builtins.input', return_value='s')
    def test_menu_search(self, mock_input):
        self.assertRaises(work_log.search_for_entry(),
                          work_log.display_menu())

    @mock.patch('builtins.input', return_value='d')
    def test_search_date(self, mock_input):
        self.assertRaises(work_log.search_by_date(),
                          work_log.search_for_entry())

    @mock.patch('builtins.input', return_value='t')
    def test_search_time_spent(self, mock_input):
        self.assertRaises(work_log.search_by_time_spent(),
                          work_log.search_for_entry())

    @mock.patch('builtins.input', return_value='n')
    def test_search_exact(self, mock_input):
        self.assertRaises(work_log.search_exact(),
                          work_log.search_for_entry())

    @mock.patch('builtins.input', return_value='p')
    def test_search_by_employee(self, mock_input):
        self.assertRaises(work_log.search_by_employee(),
                          work_log.search_for_entry())

if __name__ == '__main__':
    unittest.main()
