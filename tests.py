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
    @mock.patch('work_log.search_for_entry')
    def test_menu_called_new(self, search_mock, add_mock):
        answers = (answer for answer in ['n', 's', 'q'])
        def mock_input(prompt):
            return next(answers)
        with mock.patch('builtins.input', mock_input):
            work_log.display_menu()
        self.assertTrue(add_mock.called)
        self.assertTrue(search_mock.called)

    @mock.patch('work_log.search_by_date')
    @mock.patch('work_log.search_by_time_spent')
    @mock.patch('work_log.search_exact')
    @mock.patch('work_log.search_by_employee')
    def test_search_menu(self, employee_mock, exact_mock, time_mock,
                         date_mock):
        answers = ['p', 'n', 't', 'd']
        def mock_input(prompt):
            for answer in answers:
                yield answer
        with mock.patch('builtins.input', mock_input):
            work_log.search_for_entry()
        self.assertTrue(employee_mock.called)
        self.assertTrue(exact_mock.called)
        self.assertTrue(time_mock.called)
        self.assertTrue(date_mock.called)


if __name__ == '__main__':
    work_log.run_program('test.db')
    unittest.main()
