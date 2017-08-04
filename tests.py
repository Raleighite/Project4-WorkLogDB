import unittest

from playhouse.test_utils import test_database
from peewee import *

import work_log

test_db = SqliteDatabase(':memory:')

class DatabaseTests(unittest.TestCase):

    def test_record_creation(self):
        with test_database(test_db, (work_log.Entry)):
            work_log.new_entry({
                'Name':'Test Task',
                'Employee':'Travis',
                'Minutes Spent':10,
                'Notes':'Test note'
            })


    def test_employee_search(self):
        pass


if __name__ == '__main__':
    unittest.main()
