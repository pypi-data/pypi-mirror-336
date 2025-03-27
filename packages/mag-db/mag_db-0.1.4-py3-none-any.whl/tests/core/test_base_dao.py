import os
import unittest

from mag_tools.config.sys_config import SysConfig
from mag_tools.utils.common.random_utils import RandomUtils

from mag_db.core.base_dao import BaseDao


class TestBaseDao(unittest.TestCase):
    def setUp(self):
        SysConfig.set_root_dir(os.path.dirname(os.getcwd()))
        self.dao = BaseDao()

    def test_insert_by_sql(self):
        _id = RandomUtils.random_number(5)
        name = RandomUtils.random_string(10)

        insert_sql = f"INSERT INTO test_table (id, name) VALUES ({_id}, '{name}')"
        self.dao.insert_by_sql(insert_sql)

    def test_update_by_sql(self):
        update_sql = f"UPDATE test_table SET name = '{RandomUtils.random_string(10)}' WHERE id = 1"
        self.dao.update_by_sql(update_sql)

    def test_query_by_sql(self):
        query_sql = "SELECT id, name FROM test_table"
        results = self.dao.query_by_sql(query_sql)
        for result in results:
            print(result)

    def test_delete_by_sql(self):
        delete_sql = "DELETE FROM test_table WHERE id = 8"
        self.dao.delete_by_sql(delete_sql)

    def test_total_count(self):
        table_name = "test_table"
        count = self.dao.total_count(table_name)
        print(count)

    def test_test(self):
        result = self.dao.test()
        print(result)

if __name__ == '__main__':
    unittest.main()
