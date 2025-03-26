import unittest

from mag_db.data.column_names_mapping import ColumnNamesMapping
from mag_db.data.db_output import DbOutput
from mag_db.data.result_set_helper import ResultSetHelper


class TestResultSetHelper(unittest.TestCase):
    def setUp(self):
        self.query_result = [
            {'id': 1, 'name': 'Alice', "age": 30},
            {'id': 2, 'name': 'Bob', "age": 25},
            {'id': 3, 'name': 'Charlie', "age": 35}
        ]

        self.db_output = DbOutput()
        self.db_output.column_names = ['id', 'name', 'age']
        column_mapping = ColumnNamesMapping()
        column_mapping.put('id', int, 'id')
        column_mapping.put('name', str, 'name')
        column_mapping.put('age', int, 'age')
        self.db_output.column_name_mapping = column_mapping
        self.db_output.result_class = TestBean

    def test_to_maps(self):
        expected_result = [
            {'id': 1, 'name': 'Alice', 'age': 30},
            {'id': 2, 'name': 'Bob', 'age': 25},
            {'id': 3, 'name': 'Charlie', 'age': 35}
        ]
        result = ResultSetHelper.to_maps(self.query_result, self.db_output)
        self.assertEqual(result, expected_result)

    def test_to_beans(self):
        expected_result = [
            TestBean(id_=1, name='Alice', age=30),
            TestBean(id_=2, name='Bob', age=25),
            TestBean(id_=3, name='Charlie', age=35)
        ]
        result = ResultSetHelper.to_beans(self.query_result, self.db_output)
        self.assertEqual(result, expected_result)

class TestBean:
    def __init__(self, id_=None, name=None, age=None):
        self.id = id_
        self.name = name
        self.age = age

    def __eq__(self, other):
        if isinstance(other, TestBean):
            return self.id == other.id and self.name == other.name and self.age == other.age
        return False

if __name__ == '__main__':
    unittest.main()
