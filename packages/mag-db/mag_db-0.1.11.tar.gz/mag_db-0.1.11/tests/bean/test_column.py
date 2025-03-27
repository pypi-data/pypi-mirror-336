import unittest

from mag_db.bean.column import Column

class TestColumn(unittest.TestCase):

    def test_constructor(self):
        column = Column.of_whole_name("test_table.test_column AS test_alias")
        self.assertEqual(column.table_name, "test_table")
        self.assertEqual(column.name, "test_column")
        self.assertEqual(column.alias, "test_alias")

    def test_get_alias(self):
        column = Column(table_name="test_table", name="test_column")
        self.assertEqual(column.alias, "test_table__test_column")

    def test_get_whole_name(self):
        column = Column(table_name="test_table", name="test_column", alias="test_alias")
        self.assertEqual(column.get_whole_name(), "test_table.test_column AS test_alias")

    def test_get_short_name(self):
        column = Column(table_name="test_table", name="test_column")
        self.assertEqual(column.short_name, "test_table.test_column")

    def test_is_function(self):
        column = Column(name="SUM(test_column)")
        self.assertTrue(column.is_function)

    def test_is_empty(self):
        column = Column(name="")
        self.assertTrue(column.is_empty)

    def test_get_comment(self):
        column = Column(_comment="This is a comment with 'special' characters\".")
        self.assertEqual(column.comment, "This is a comment with special characters.")

    def test_is_unique(self):
        column = Column(uniques=["unique1", "unique2"])
        self.assertTrue(column.is_unique)

if __name__ == '__main__':
    unittest.main()
