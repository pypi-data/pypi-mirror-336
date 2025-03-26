import unittest

from mag_db.bean.table import Table
from parser.sql_parser import SqlParser
from utils.column_utils import ColumnUtils


class TestSqlParser(unittest.TestCase):

    def test_get_tables(self):
        sql = "SELECT * FROM test_table"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser(sql).tables], expected_tables)

        sql = "INSERT INTO test_table (col1, col2) VALUES (1, 2)"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser(sql).tables], expected_tables)

        sql = "UPDATE test_table SET col1 = 1 WHERE col2 = 2"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser(sql).tables], expected_tables)

        sql = "DELETE FROM test_table WHERE col1 = 1"
        expected_tables = ["test_table"]
        self.assertEqual([table.name for table in SqlParser(sql).tables], expected_tables)

    def test_get_column_names(self):
        sql = "SELECT col1, col2 FROM test_table"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser(sql).column_names, expected_columns)

        sql = "INSERT INTO test_table (col1, col2) VALUES (1, 2)"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser(sql).column_names, expected_columns)

        sql = "UPDATE test_table SET col1 = 1, col2 = 2 WHERE col3 = 3"
        expected_columns = ["col1", "col2"]
        self.assertEqual(SqlParser(sql).column_names, expected_columns)

    def test_convert_column_name(self):
        sql = "SELECT t.col1, t.col2 FROM test_table AS t"
        tables = [Table(name="test_table", alias="t")]
        expected_sql = "SELECT test_table.col1, test_table.col2 FROM test_table AS t"
        self.assertEqual(ColumnUtils.convert_column_name(sql, tables), expected_sql)

if __name__ == '__main__':
    unittest.main()
