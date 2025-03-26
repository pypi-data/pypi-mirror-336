import unittest

from mag_db.bean.table import Table
from mag_db.utils.column_utils import ColumnUtils


class TestColumnUtils(unittest.TestCase):
    def test_convert_column_name(self):
        sql = "INSERT INTO table_name1 AS t (t.column1 AS c1, t.column2 AS c2 ) VALUES ('value1', 'value2');"
        table_name = "table_name1"
        table_alias = "t"

        converted_sql = ColumnUtils.convert_column_name(sql, [Table(table_name, alias=table_alias)])
        print(converted_sql)

if __name__ == '__main__':
    unittest.main()
