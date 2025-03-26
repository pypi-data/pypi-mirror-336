import re
from typing import List, Optional, Type

from mag_tools.exception.dao_exception import DaoException
from mag_tools.model.symbol import Symbol

from bean.column import Column
from mag_db.bean.table import Table
from mag_db.model.operator_type import OperatorType
from model.sql_type import SqlType
from utils.column_utils import ColumnUtils


class TableUtils:
    @staticmethod
    def get_table_from_sql(create_sql: str):
        table = Table()

        sql = create_sql.replace(OperatorType.CREATE_TABLE.code, "").strip()

        idx = sql.find(Symbol.OPEN_PAREN.code)
        if idx <= 0:
            raise DaoException(f"建表SQL语句有错：{create_sql}")

        table.names = [sql[:idx].strip()]

        sql = sql[idx + 1:]
        idx = sql.rfind(Symbol.CLOSE_PAREN.code)
        if idx <= 0:
            raise DaoException(f"建表SQL语句有错：{create_sql}")

        sql = sql[:idx]

        idx = sql.find(OperatorType.PRIMARY_KEY.code)
        if idx > 0:
            table.primary_key = sql[idx:].replace(Symbol.OPEN_PAREN.code, "").replace(Symbol.CLOSE_PAREN.code, "")
            sql = sql[:idx].strip()

        column_infos = re.split(r',\s*(?![^()]*\))', sql)
        columns = TableUtils.to_column(column_infos)

        table.set_columns(columns)

        return table

    @staticmethod
    def to_column(column_infos: List[str]):
        columns = []

        for column_info in column_infos:
            column = Column()

            column_info = column_info.strip()

            idx = column_info.find(Symbol.BLANK.code)
            if idx <= 0:
                raise DaoException("列描述语句错误")

            name = column_info[:idx]
            column.name = name

            column_info = column_info[idx + 1:].upper()

            idx = column_info.find(Symbol.BLANK.code)
            if idx <= 0:
                raise DaoException("列描述语句错误")

            type_str = column_info[:idx]
            column_info = column_info[idx + 1:]

            idx = type_str.find(Symbol.OPEN_PAREN.code)
            if idx > 0:
                idx_close = type_str.find(Symbol.CLOSE_PAREN.code)
                size = type_str[idx + 1:idx_close]
                column.column_size = int(size)
                type_str = type_str[:idx]

            column.sql_type = SqlType.of_code(type_str)
            column.can_null = OperatorType.NOT_NULL not in column_info
            column.auto_increment = OperatorType.AUTO_INCREMENT.code in column_info

            columns.append(column)

        return columns

    @staticmethod
    def to_table(bean_cls: Type, table_name: str, comment: Optional[str] = None, auto_increment_value: bool = True):
        table = Table()
        table.names = [table_name]

        fields = [field for field in dir(bean_cls) if not callable(getattr(bean_cls, field)) and not field.startswith("__")]
        table.__columns = [ColumnUtils.to_column(field) for field in fields]
        table.comment = comment
        table.auto_increment = auto_increment_value

        return table

    @staticmethod
    def clear_table_name(name):
        return re.sub(r'[^\w]', '', name.strip()) if name else None
