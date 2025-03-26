from typing import List

from mag_db.builder.base_sql import BaseSql
from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.model.operator_type import OperatorType
from mag_tools.model.symbol import Symbol

class Alter(BaseSql):
    def __init__(self, table_name: str, columns: List[Column], operator_type: OperatorType):
        super().__init__()

        table = Table(table_name)

        self.append_operator(OperatorType.ALTER_TABLE).append_tables([table])

        if operator_type == OperatorType.ADD:
            for column in columns:
                self.append_operator(OperatorType.ADD).append_whole_column(column)
        elif operator_type == OperatorType.DROP_COLUMN:
            for column in columns:
                self.append_operator(OperatorType.DROP_COLUMN).append_column(column, False, False).append_symbol(Symbol.COMMA)

        self.remove_last_keyword(",")

    @staticmethod
    def add(table_name: str, columns: List[Column]):
        return Alter(table_name, columns, OperatorType.ADD)

    @staticmethod
    def drop(table_name: str, columns: List[Column]):
        return Alter(table_name, columns, OperatorType.DROP_COLUMN)
