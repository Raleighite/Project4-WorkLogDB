import unittest

import work_log

from peewee import *

class DatabaseTests(unittest.TestCase):
    def setup(self):
        db = SqliteDatabase("test.db")

    def test_record_creation(self):
        work_log.new_entry({
            'Name':'Test Task',
            'Employee':'Travis',
            'Minutes Spent': 10,
            'Notes': 'Test note'
        })
        self.assertTrue(work_log.Entry.get(title='Test Task'))

    def test_employee_search(self):
        pass


if __name__ == '__main__':
    unittest.main()
