import os.path
import random
import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar

from mag_tools.bean.easy_map import EasyMap
from mag_tools.config.sys_config import SysConfig

from mag_db.core.simple_dao import SimpleDao
from mag_db.builder.where import Where

T = TypeVar('T')

@dataclass
class Test:
    name: str = None
    age: int = None
    open_date: datetime = None
    id: int = None

class TestDao(SimpleDao):
    def __init__(self):
        super().__init__(['test_table'], Test, primary_key_column='id', auto_increment=True)


class TestSimpleDao(unittest.TestCase):
    def setUp(self):
        SysConfig.set_root_dir(os.path.dirname(os.getcwd()))

    def test_insert(self):
        age = random.randint(1, 100)
        bean = Test("Alice", age)
        id_ = TestDao().insert(bean)

        result = TestDao().query_map(Where(f"Where age = {age} and name = 'Alice'"))

        self.assertEqual(result.get('id'), id_)

    def test_insert_map(self):
        age = random.randint(1, 100)
        field = {"age": age, "name": "Alice"}
        id_ = TestDao().insert_map(EasyMap(field))
        result = TestDao().query_map(Where(f"Where age = {age} and name = 'Alice'"))

        self.assertEqual(result.get('id'), id_)

    def test_insert_beans(self):
        age1 = random.randint(1, 100)
        age2 = random.randint(1, 100)
        age3 = random.randint(1, 100)

        beans = [Test("Alice", age1, datetime.now()), Test("Bob", age2), Test("Peter", age3)]
        ids = TestDao().insert_beans(beans)

        where = Where(f"Where age = {age1} and name = 'Alice'")
        id1 = TestDao().query(Test, where).id

        where = Where(f"Where age = {age2} and name = 'Bob'")
        id2 = TestDao().query(Test, where).id

        where = Where(f"Where age = {age3} and name = 'Peter'")
        id3 = TestDao().query(Test, where).id

        self.assertEqual([id1, id2, id3], ids)

    def test_insert_maps(self):
        age1 = random.randint(1, 100)
        age2 = random.randint(1, 100)
        age3 = random.randint(1, 100)

        fields = [{"age": age1, "name": "Alice"}, {"age": age2, "name": "Bob"}, {"age": age3, "name": "Peter"}]
        ids = TestDao().insert_maps([EasyMap(field) for field in fields])

        where = Where(f"Where age = {age1} and name = 'Alice'")
        id1 = TestDao().query(Test, where).id

        where = Where(f"Where age = {age2} and name = 'Bob'")
        id2 = TestDao().query(Test, where).id

        where = Where(f"Where age = {age3} and name = 'Peter'")
        id3 = TestDao().query(Test, where).id

        self.assertEqual([id1, id2, id3], ids)

    def test_delete(self):
        age_1 = random.randint(100, 10000)
        bean = Test("Alice", age_1)
        result = TestDao().insert(bean)
        print(f"插入的ID：{result}")

        where = Where(f"age = {age_1} AND name = 'Alice'")
        result = TestDao().delete(where)
        self.assertEqual(result, 1)

    def test_delete_by_id(self):
        age_1 = random.randint(100, 10000)
        bean = Test("Alice", age_1)
        id_ = TestDao().insert(bean)
        print(f"插入的ID：{id_}")

        result = TestDao().delete_by_id(id_)
        self.assertEqual(result, 1)

    def test_delete_by_ids(self):
        age1 = random.randint(1, 100)
        age2 = random.randint(1, 100)

        fields = [{"age": age1, "name": "Alice"}, {"age": age2, "name": "Bob"}]
        ids = TestDao().insert_maps([EasyMap(field) for field in fields])

        result = TestDao().delete_by_ids(ids)
        self.assertEqual(result, 2)

    def test_clear(self):
        result = TestDao().clear()
        print(result)

    def test_update(self):
        age = random.randint(1, 100)
        bean = Test("Alice", age)
        id_ = TestDao().insert(bean)

        bean.age = 1000
        where = Where(f"id = {id_}")
        result = TestDao().update(bean, where)
        self.assertEqual(result, 1)

    def test_update_by_id(self):
        age = random.randint(1, 1000)
        bean = Test("Alice", age)
        id_ = TestDao().insert(bean)

        bean.age = 1001
        result = TestDao().update_by_id(bean, id_)
        self.assertEqual(result, 1)

    def test_update_by_id_of_bean(self):
        age = random.randint(1, 1000)
        bean = Test("Alice", age)
        id_ = TestDao().insert(bean)

        bean.id = id_
        bean.age = 1005

        result = TestDao().update_by_id_of_bean(bean)
        self.assertEqual(result, 1)

    def test_update_beans(self):
        age1 = random.randint(1, 100)
        age2 = random.randint(1, 100)
        bean1 = Test("Alice", age1, datetime.now())
        bean2 = Test("Bob", age2, datetime.now())
        ids = TestDao().insert_beans([bean1, bean2])
        bean1.id = ids[0]
        bean1.age = 1009
        bean2.id = ids[1]
        bean2.age = 1010

        result = TestDao().update_beans([bean1, bean2])
        self.assertEqual(result, 2)

    def test_update_map(self):
        age1 = random.randint(1, 100)
        bean1 = Test("Alice", age1, datetime.now())
        ids = TestDao().insert_beans([bean1])

        field_map = {"name": "Alice", "age": 1020}
        where = Where(f"id = {ids[0]}")
        result = TestDao().update_map(field_map, where)
        self.assertEqual(result, 1)

    def test_update_map_by_id(self):
        age1 = random.randint(1, 100)
        map1 = EasyMap().add("name", "Alice").add("age", age1).add("open_date", datetime.now())
        ids = TestDao().insert_maps([map1])

        field_map = {"name": "Alice", "age": 1099}
        result = TestDao().update_map_by_id(field_map, ids[0])

        self.assertEqual(result, 1)

    def test_update_map_by_id_of_map(self):
        age1 = random.randint(1, 100)
        map1 = EasyMap().add("name", "Alice").add("age", age1).add("open_date", datetime.now())
        ids = TestDao().insert_maps([map1])

        field_map = {"id": f"{ids[0]}", "name": "Alice", "age": 1199}
        result = TestDao().update_map_by_id_of_map(field_map)
        self.assertEqual(result, 1)

    def test_update_maps(self):
        age1 = random.randint(1, 100)
        age2 = random.randint(1, 100)
        map1 = EasyMap().add("name", "Alice").add("age", age1).add("open_date", datetime.now())
        map2 = EasyMap().add("name", "Bob").add("age", age2).add("open_date", datetime.now())
        ids = TestDao().insert_maps([map1, map2])

        map1 = {"id": ids[0], "age": 1009, "open_date": datetime.now()}
        map2 = {"id": ids[1], "age": 1010, "open_date": datetime.now()}

        result = TestDao().update_maps([map1, map2])
        self.assertEqual(result, 2)

    def test_query(self):
        where = Where.builder().column_value('id', 99669)
        result = TestDao().query(Test, where)
        print(result)

    def test_query_map(self):
        where = Where.builder().column_value('id', 99669)
        result = TestDao().query_map(where)
        print(result)

    def test_query_by_id(self):
        result = TestDao().query_by_id(Test, 99669)
        print(result)

    def test_query_map_by_id(self):
        result = TestDao().query_map_by_id(99669)
        print(result)

    def test_list(self):
        result = TestDao().list(Test, Where("`id` = 99669"))
        for row in result:
            print(row)

    def test_list_maps(self):
        result = TestDao().list_maps(Where("`id` = 99669"))
        for row in result:
            print(row)

    def test_list_all(self):
        result = TestDao().list_all(Test)
        for row in result:
            print(row)

    def test_list_all_maps(self):
        result = TestDao().list_all_maps()
        for row in result:
            print(row)

    def test_get_latest_time(self):
        dt = TestDao().get_latest_time(Where(), 'open_date')
        print(dt)

if __name__ == '__main__':
    unittest.main()
