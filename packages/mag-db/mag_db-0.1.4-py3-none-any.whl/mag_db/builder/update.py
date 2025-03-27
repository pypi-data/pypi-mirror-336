from typing import List

from mag_tools.model.symbol import Symbol

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.builder.base_sql import BaseSql
from mag_db.builder.where import Where
from mag_db.model.operator_type import OperatorType


class Update(BaseSql):
    """
    UPDATE语句操作类

    @description: 用于构建UPDATE语句。
    @version: v1.0
    @date: 2019/8/30
    """
    def __init__(self, table_names: List[str], column_names: List[str], where: Where):
        """
        构造方法

        :param table_names: the database table names
        :param column_names: the column names which need to update
        :param where: the string conditions, for example: WHERE condition1 = ? AND condition2 = ?
        """
        super().__init__()

        self.append_operator(OperatorType.UPDATE).append_tables([Table(name) for name in table_names])
        self.append_set_columns(self.to_columns(column_names))
        if where:
            self.append_condition(where)

    def append_set_columns(self, column_names: List[Column]):
        """
        添加列名设置

        :param column_names: the column name which need to update
        """
        self.append_operator(OperatorType.SET)

        for i, column in enumerate(column_names):
            self.append_column(column, True, False)
            self.append_symbol(Symbol.EQUAL)
            self.append_symbol(Symbol.PLACE_HOLDER)
            if i < len(column_names) - 1:
                self.append_symbol(Symbol.COMMA)

        return self