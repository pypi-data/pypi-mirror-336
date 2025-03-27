from typing import List

from mag_tools.model.symbol import Symbol

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.builder.base_sql import BaseSql
from mag_db.model.operator_type import OperatorType
from mag_db.model.relation import Relation


class Insert(BaseSql):
    """
    INSERT语句操作类

    @description: 用于构建INSERT语句。
    @version: v1.0
    @date: 2019/8/30
    """
    def __init__(self, table_names: List[str], column_names: List[str], record_count: int, duplicate_update: bool = False):
        """
        构造方法

        :param table_names: the database table name
        :param column_names: the list of column names which need to be inserted
        :param record_count: the count of records
        :param duplicate_update: 是否更新重复记录
        """
        super().__init__()

        self.append_operator(OperatorType.INSERT).append_tables([Table(name) for name in table_names])
        self.__append_columns(column_names, record_count)

        if duplicate_update:
            self.append_operator(OperatorType.DUPLICATE_UPDATE)

            is_first = True
            for column_name in column_names:
                if is_first:
                    is_first = False
                else:
                    self.append_symbol(Symbol.COMMA)

                self.append_column(Column(column_name), True, False).append_relation(Relation.EQUAL).append_operator(OperatorType.VALUES).append_symbol(Symbol.OPEN_PAREN).append_column(Column(column_name), True, False).append_symbol(Symbol.CLOSE_PAREN)

    def __append_columns(self, column_names: List[str], record_count: int) -> 'Insert':
        is_multi_table = len(self.tables) > 1

        self.append_with_paren(self.to_columns(column_names), is_multi_table).append_operator(OperatorType.VALUES)
        self.__append_values(len(column_names), record_count)

        return self

    def __append_values(self, param_count: int, record_count: int):
        """
        return the value part of a sql prepareStatement

        :param param_count: the size of question mark, aka ?
        :param record_count: the size of records
        """
        for i in range(record_count):
            if i > 0:
                self.append_symbol(Symbol.COMMA)
            self.append_symbol(Symbol.OPEN_PAREN)

            for j in range(param_count - 1):
                self.append_symbol(Symbol.PLACE_HOLDER)
                self.append_symbol(Symbol.COMMA)

            if param_count > 0:
                self.append_symbol(Symbol.PLACE_HOLDER)

            self.append_symbol(Symbol.CLOSE_PAREN)