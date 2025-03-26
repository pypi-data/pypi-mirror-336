import unittest
from decimal import Decimal
from datetime import date, time, datetime

from mag_db.model.sql_type import SqlType


class TestSqlType(unittest.TestCase):

    def test_of_class(self):
        self.assertEqual(SqlType.of_class(int), SqlType.INT)
        self.assertEqual(SqlType.of_class(float), SqlType.FLOAT)
        self.assertEqual(SqlType.of_class(Decimal), SqlType.DECIMAL)
        self.assertEqual(SqlType.of_class(bool), SqlType.BOOLEAN)
        self.assertEqual(SqlType.of_class(str, 100), SqlType.CHAR)
        self.assertEqual(SqlType.of_class(str, 5000), SqlType.VARCHAR)
        self.assertEqual(SqlType.of_class(str, 60000), SqlType.TEXT)
        self.assertEqual(SqlType.of_class(str, 10000000), SqlType.MEDIUMTEXT)
        self.assertEqual(SqlType.of_class(str, 20000000), SqlType.LONGTEXT)
        self.assertEqual(SqlType.of_class(date), SqlType.DATE)
        self.assertEqual(SqlType.of_class(time), SqlType.TIME)
        self.assertEqual(SqlType.of_class(datetime), SqlType.DATETIME)

    def test_get_class(self):
        self.assertEqual(SqlType.get_class("INT"), int)
        self.assertEqual(SqlType.get_class("FLOAT"), float)
        self.assertEqual(SqlType.get_class("DECIMAL"), Decimal)
        self.assertEqual(SqlType.get_class("BOOLEAN"), bool)
        self.assertEqual(SqlType.get_class("CHAR"), str)
        self.assertEqual(SqlType.get_class("DATE"), date)
        self.assertEqual(SqlType.get_class("TIME"), time)
        self.assertEqual(SqlType.get_class("DATETIME"), datetime)

    def test_str(self):
        self.assertEqual(SqlType.INT.code, "INT")
        self.assertEqual(str(SqlType.FLOAT), "FLOAT")
        self.assertEqual(str(SqlType.DECIMAL), "DECIMAL")
        self.assertEqual(str(SqlType.BOOLEAN), "BOOLEAN")
        self.assertEqual(str(SqlType.CHAR), "CHAR")
        self.assertEqual(str(SqlType.DATE), "DATE")
        self.assertEqual(str(SqlType.TIME), "TIME")
        self.assertEqual(str(SqlType.DATETIME), "DATETIME")

if __name__ == '__main__':
    unittest.main()
