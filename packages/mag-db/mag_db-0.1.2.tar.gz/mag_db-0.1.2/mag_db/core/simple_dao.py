from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from mag_tools.bean.easy_map import EasyMap
from mag_tools.exception.dao_exception import DaoException
from mag_tools.utils.common.list_utils import ListUtils

from mag_db.bean.primary_key import PrimaryKey
from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.bean.db_list import DbList
from mag_db.bean.table_info import TableInfo
from mag_db.builder.delete import Delete
from mag_db.builder.insert import Insert
from mag_db.builder.select import Select
from mag_db.builder.update import Update
from mag_db.builder.where import Where
from mag_db.core.base_dao import BaseDao
from mag_db.model.relation import Relation
from mag_db.sql.index_delete_executor import IndexDeleteExecutor
from mag_db.sql.index_insert_executor import IndexInsertExecutor
from mag_db.sql.index_query_executor import IndexQueryExecutor
from mag_db.sql.index_update_executor import IndexUpdateExecutor

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class SimpleDao(BaseDao):
    def __init__(self, table_names: List[str], bean_type: Type = None, column_names: List[str] = None,
                 primary_key_column: Optional[str] = None, distinct: bool = False, column_name_map: Optional[Dict[str, str]] = None,
                 auto_increment: bool = False):
        super().__init__()

        if not column_names and bean_type and hasattr(bean_type, '__annotations__'):
            column_names = list(bean_type.__annotations__.keys())

        tables = [Table(name) for name in table_names]
        columns = [Column(name) for name in column_names]
        primary_key = PrimaryKey([primary_key_column]) if primary_key_column else None

        self._table_info = TableInfo(tables, columns, primary_key, distinct=distinct, column_name_map=column_name_map, auto_increment=auto_increment)

    """
    常用的DAO操作类

      @version 1.0
      @Description 提供基本数据库操作, 如插入、更新等。
      注：SimpleDao类只提供简单的单表数据库操作，对复杂的SQL或多表操作可直接写SQL或继承BaseDao来完成。
      <p>
      数据源名称，其值必须与配置文件DBConfig.xml中的某个数据源名称一致。DBConfig.xml中可以定义多个数据源，
      但每个Dao基类只能对应其中一个数据源。数据源名称应当常量定义,以便事务处理使用。
      <p>
      Copyright: Copyright (c) 2015
      Company:
    """

    def insert(self, bean: T) -> int:
        """
         插入一条记录

         @param bean 要插入的数据
         @param <T>   列数值Bean类型
        """
        if isinstance(bean, list):
            raise DaoException("该方法只能插入单条数据")

        return self.insert_beans([bean])[0]

    def insert_map(self, field: EasyMap[K, V]) -> int:
        """
        插入操作
        """
        return self.insert_maps([field])[0]

    def insert_beans(self, beans: List[T]) -> List[int]:
        """
        多记录插入操作
        """
        return self.__do_insert_beans(beans)

    def insert_maps(self, fields: List[EasyMap[K, V]]) -> List[int]:
        """
        多记录插入操作
        """
        return self.__do_insert_maps(fields)

    def delete(self, where: Where) -> int:
        if where is None or where.is_empty:
            return 0

        delete_sql = Delete(self._table_info.table_names, where)
        delete = IndexDeleteExecutor(delete_sql.__str__(), self._session)
        if where.has_fields():
            delete.set_fields_of_where(where.fields)
        return delete.execute()

    def delete_by_id(self, id_: Any) -> int:
        if isinstance(id, list):
            raise DaoException("该方法只能删除单条数据")

        where = Where.builder().column(self._table_info.default_primary_key, Relation.EQUAL, id_)
        return self.delete(where)

    def delete_by_ids(self, ids: List[Any]) -> int:
        where = Where.builder().in_list(self._table_info.default_primary_key, ids)
        return self.delete(where)

    def clear(self) -> int:
        delete_sql = Delete(self._table_info.table_names, Where())
        delete = IndexDeleteExecutor(delete_sql.__str__(), self._session)
        return delete.execute()

    def update(self, param_bean: T, where: Where):
        update_sql = Update(self._table_info.table_names, self._table_info.get_column_names(), where)

        update = IndexUpdateExecutor(update_sql.__str__(), self._session)
        update.set_beans([param_bean], self._table_info.get_column_names(), self._table_info.column_name_map)
        if where.has_fields():
            update.set_fields_of_where(where.fields)

        return update.execute()

    def update_by_id(self, param_bean: T, id_: Any) -> int:
        where = Where.builder().column(self._table_info.default_primary_key, Relation.EQUAL, id_)
        return self.update(param_bean, where)

    def update_by_id_of_bean(self, param_bean: T) -> int:
        id_ = getattr(param_bean, self._table_info.default_primary_key)
        if id_ is None:
            raise DaoException(f"主键[{self._table_info.default_primary_key}]不存在")

        return self.update_by_id(param_bean, id_)

    def update_beans(self, param_beans: List[T]) -> int:
        """
        根据主键更新多个Bean
        """
        num = 0
        for bean in param_beans:
            num += self.update_by_id_of_bean(bean)
        return num

    def update_map(self, field_map: Dict[K, V], where: Where) -> int:
        update_sql = Update(self._table_info.table_names, self._table_info.get_column_names(), where)
        update = IndexUpdateExecutor(update_sql.__str__(), self._session)
        update.set_maps([field_map], self._table_info.get_column_names())
        if where.has_fields():
            update.set_fields_of_where(where.fields)

        return update.execute()

    def update_map_by_id(self, field_map: Dict[K, V], id_: Any) -> int:
        where = Where.builder().column(self._table_info.default_primary_key, Relation.EQUAL, id_)
        return self.update_map(field_map, where)

    def update_map_by_id_of_map(self, field_map: Dict[K, V]) -> int:
        id_ = field_map.get(self._table_info.default_primary_key, None)
        if id_ is None:
            raise DaoException(f"主键[{self._table_info.default_primary_key}]不存在")

        return self.update_map_by_id(field_map, id_)

    def update_maps(self, field_maps: List[Dict[K, V]]) -> int:
        num = 0
        for field_map in field_maps:
            num += self.update_map_by_id_of_map(field_map)
        return num

    def query(self, bean_class: type, where: Where) -> T:
        """
        查询数据库符合条件的指定记录
        """
        select = self.__get_select(where)

        query = IndexQueryExecutor(select.__str__(), self._session)
        if where.has_fields():
            query.set_fields_of_where(where.fields)

        return query.execute_bean(bean_class, self._table_info.get_column_names(True), self._table_info.column_name_map)

    def query_map(self, where: Where) -> Dict[str, T]:
        """
        查询数据库，查询结果保存在一个Map
        """
        select = self.__get_select(where)

        query = IndexQueryExecutor(select.__str__(), self._session)
        if where.has_fields():
            query.set_fields_of_where(where.fields)

        return query.execute_map(self._table_info.get_column_names(True))

    def query_by_id(self, bean_class: type, id_: str or int) -> T:
        """
        根据主键查询符合条件的指定记录
        """
        where = Where.builder().column(self._table_info.default_primary_key, Relation.EQUAL, id_)
        return self.query(bean_class, where)

    def query_map_by_id(self, id_: str or int) -> Dict[str, Any]:
        """"
        根据主键查询
        """
        where = Where.builder().column(self._table_info.default_primary_key, Relation.EQUAL, id_)
        return self.query_map(where)

    def list(self, bean_class: type, where: Where) -> DbList[T]:
        """
        按条件列表数据库记录
        """
        select = self.__get_select(where)

        query = IndexQueryExecutor(select.__str__(), self._session)
        if where.has_fields():
            query.set_fields_of_where(where.fields)

        if where.is_page_query:
            return query.execute_beans_by_page(bean_class, self._table_info.get_column_names(True), self._table_info.column_name_map, where.page)
        else:
            return query.execute_beans(bean_class, self._table_info.get_column_names(True), self._table_info.column_name_map)

    def list_maps(self, where: Where) -> DbList[Dict[str, Any]]:
        select = self.__get_select(where)

        query = IndexQueryExecutor(select.__str__(), self._session)
        if where.has_fields():
            query.set_fields_of_where(where.fields)

        if where.is_page_query:
            return query.execute_maps_by_page(self._table_info.get_column_names(True), where.page)
        else:
            return query.execute_maps(self._table_info.get_column_names(True))

    def list_all(self, bean_class: type) -> 'DbList[T]':
        """
        列表数据库的全部记录
        :param bean_class: Bean类型
        """
        select = self.__get_select(Where())
        query = IndexQueryExecutor(select.__str__(), self._session)
        return query.execute_beans(bean_class, self._table_info.get_column_names(True), self._table_info.column_name_map)

    def list_all_maps(self) -> DbList[Dict[str, Any]]:
        select = self.__get_select(Where())
        query = IndexQueryExecutor(select.__str__(), self._session)
        return query.execute_maps(self._table_info.get_column_names(True))

    def get_latest_time(self, where: Where, order_by: str) -> Optional[datetime]:
        """
        查询表中最新记录的时间字段
        :param where: 查询条件
        :param order_by: 排序列名
        """
        where = where if where else Where()
        where.order(False, order_by).limit(1)

        record = self.query_map(where)
        return record.get(order_by, None) if record else None

    def __do_insert_beans(self, beans: List[T]) -> List[int]:
        """
        多记录插入操作
        当要插入的数据记录过多时，则分批插入
        @return 如有自增的主键，则返回主键值列表；否则返回null"""
        if not beans or len(beans) == 0:
            raise DaoException("至少要插入一条记录")

        blocks = ListUtils.split(beans, int(self._session.max_insert))

        insert_sql = Insert(self._table_info.table_names, self._table_info.get_column_names(), len(blocks[0]))
        insert = IndexInsertExecutor(insert_sql.__str__(), self._session)
        column_names_mapping = self._table_info.column_name_map

        insert_ids = []
        for i, block in enumerate(blocks):
            # 最后一块因记录数目不同，要重新生成insert
            if i == len(blocks) - 1:
                # insert_sql = Insert(self._table_info.table_names, self._table_info.get_column_names(), len(block))
                insert_sql = Insert(self._table_info.table_names, self._table_info.get_column_names(), 1)
                insert = IndexInsertExecutor(insert_sql.__str__(), self._session)

            insert_ids.extend(self.__insert_part_of_beans(insert, block, column_names_mapping))

        return insert_ids

    def __do_insert_maps(self, field_maps: List[EasyMap[K, V]]) -> List[int]:
        """
        多记录插入操作
        当要插入的数据记录过多时，则分批插入
        @return 如有自增的主键，则返回主键值列表；否则返回null
        """
        if not field_maps or len(field_maps) == 0:
            raise DaoException("至少要插入一条记录")

        blocks = ListUtils.split(field_maps, int(self._session.max_insert))
        insert_sql = Insert(self._table_info.table_names, self._table_info.get_column_names(), len(blocks[0]))
        insert = IndexInsertExecutor(insert_sql.__str__(), self._session)

        insert_ids = []
        for i, block in enumerate(blocks):
            if i == len(blocks) - 1:
                insert_sql = Insert(self._table_info.table_names, self._table_info.get_column_names(), len(block))
                insert = IndexInsertExecutor(insert_sql.__str__(), self._session)

            insert_ids.extend(self.__insert_part_of_maps(insert, block))

        return insert_ids

    def __insert_part_of_beans(self, insert: IndexInsertExecutor, beans: List[T], column_name_map: dict[str, str]) -> List[int]:
        insert.clear_parameters()
        insert.set_beans(beans, self._table_info.get_column_names(), column_name_map)

        return insert.execute()

    def __insert_part_of_maps(self, insert: IndexInsertExecutor, field_maps: List[EasyMap[K, V]]) -> List[int]:
        insert.clear_parameters()
        for field_map in field_maps:
            insert.set_maps([field_map], self._table_info.get_column_names())

        return insert.execute()

    def __get_select(self, where: Optional[Where]) -> Select:
        select = Select(self._table_info.table_names, self._table_info.get_column_names(True), where)
        if self._table_info.distinct:
            select.set_distinct()
        return select
