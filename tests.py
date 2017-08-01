import unittest

import work_log

class DatabaseSearchTests(unittest.TestCase):
    def setup(self):


    def test_employee_search(self):
        self.assertIn(work_log.search_by_employee("Jack"),

