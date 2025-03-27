import unittest

from mag_tools.model.base_enum import BaseEnum

from mag_db.handler.int_type_handler import IntTypeHandler
from mag_db.handler.string_type_handler import StringTypeHandler
from mag_db.utils.dao_utils import DaoUtils


class TestIntEnum(BaseEnum):
    VALUE1 = (1, '1吧')
    VALUE2 = (2, '2吧')

class TestStrEnum(BaseEnum):
    VALUE1 = ('1', '1吧')
    VALUE2 = ('2', '2吧')


class TestDaoUtils(unittest.TestCase):
    def test_get_type_handler_with_int_enum(self):
        handler = DaoUtils.get_type_handler(TestIntEnum)
        self.assertIsInstance(handler, IntTypeHandler)

    def test_get_type_handler_with_str_enum(self):
        handler = DaoUtils.get_type_handler(TestStrEnum)
        self.assertIsInstance(handler, StringTypeHandler)

    def test_get_type_handler_with_int(self):
        handler = DaoUtils.get_type_handler(int)
        self.assertIsInstance(handler, IntTypeHandler)

    def test_get_type_handler_with_str(self):
        handler = DaoUtils.get_type_handler(str)
        self.assertIsInstance(handler, StringTypeHandler)

if __name__ == '__main__':
    unittest.main()
