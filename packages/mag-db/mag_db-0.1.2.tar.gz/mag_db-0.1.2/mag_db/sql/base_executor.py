from typing import Any, Dict, List, Optional

import pymysql
from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType
from mag_tools.model.symbol import Symbol
from pymysql import Connection
from pymysql.cursors import Cursor

from mag_db.core.db_session import DBSession
from mag_db.core.transaction import Transaction
from mag_db.data.index_parameters import IndexParameters, K, T, V


class BaseExecutor:
    def __init__(self, sql: str, session: DBSession):
        if not sql:
            raise ValueError('sql cannot be empty')

        self._sql = sql
        self._session = session
        self._indexParameters = IndexParameters()

    def get_connection(self, tx: Optional[Transaction] = None)->Connection:
        con = None

        try:
            # 取得当前未结束的事务
            if tx:
                tx.assert_open()
                # 如果SQL操作属于某个事务，则从该事务中取得连接
                con = tx.connection
            else:
                # 无事务则直接取得新的连接
                if self._session is None:
                    raise DaoException("找不到有用数据库会话")

                con = self._session.connect()

            if con is None:
                raise DaoException("数据库连接不能为空")
        except DaoException as e:
            Logger.throw(LogType.DAO, f"取数据库连接失败: {str(e)}")

        return con

    @classmethod
    def close_connection(cls, con: Connection, tx: Transaction = None, cursor: Cursor = None):
        try:
            if cursor:
                cursor.close()
        except pymysql.MySQLError:
            pass

        try:
            # 无事务则直接关闭连接, 否则数据库连接随相应事务关闭而关闭
            if tx is None and con:
                con.close()
        except pymysql.MySQLError:
            pass

        try:
            if tx:
                tx.close()
        except pymysql.MySQLError:
            pass

    def prepare(self)->Optional[tuple[tuple[Any,...], ...]]:
        if self._indexParameters and not self._indexParameters.is_empty():
            return self._indexParameters.get_values()
        return None

    def check(self) -> None:
        num_of_holder = self._sql.count(Symbol.PLACE_HOLDER.code)
        num_of_row = self._indexParameters.row_count
        num_of_field = self._indexParameters.field_num

        if num_of_holder * num_of_row != self._indexParameters.sum_of_params+ num_of_field:
            msg = (f"参数个数不匹配(总参数={self._indexParameters.sum_of_params}，占位符={num_of_holder}, 行数={num_of_row}，条件字段={num_of_field})\n"
                   f"参数为：{self._indexParameters.parameters}")
            Logger.throw(LogType.DAO, msg)

    def clear_parameters(self) -> None:
        self._indexParameters.clear()

    def set_string(self, parameter: str) -> None:
        self._indexParameters.set_string(parameter)

    def set_bytes(self, parameter: bytes) -> None:
        self._indexParameters.set_bytes(parameter)

    def set_date(self, parameter) -> None:
        self._indexParameters.set_date(parameter)

    def set_time(self, parameter) -> None:
        self._indexParameters.set_time(parameter)

    def set_datetime(self, parameter) -> None:
        self._indexParameters.set_datetime(parameter)

    def set_bool(self, parameter: bool) -> None:
        self._indexParameters.set_bool(parameter)

    # def set_bean(self, parameter: T, column_names, column_name_map: Dict[str, str]) -> None:
    #     self._indexParameters.set_bean(parameter, column_names, column_name_map)

    def set_beans(self, parameter: List[T], column_names, column_name_map: Dict[str, str]) -> None:
        self._indexParameters.set_beans(parameter, column_names, column_name_map)

    # def set_map(self, parameter: Dict[K, V], column_names) -> None:
    #     self._indexParameters.set_field_map(parameter, column_names)

    def set_maps(self, parameter: List[Dict[K, V]], column_names) -> None:
        self._indexParameters.set_field_maps(parameter, column_names)

    def set_fields_of_where(self, fields: List) -> None:
        self._indexParameters.set_fields_of_where(fields)