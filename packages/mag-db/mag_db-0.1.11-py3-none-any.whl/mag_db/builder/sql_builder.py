from typing import List, Optional

from mag_tools.model.symbol import Symbol

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.model.operator_type import OperatorType
from mag_db.model.relation import Relation


class SqlBuilder:
    def __init__(self, sql: Optional[str] = None):
        """
        初始化SqlBuilder类，接受一个可选的SQL字符串。
        :param sql: 可选的SQL字符串
        """
        self.string_builder = [sql] if sql else []

    def append_string(self, string: str):
        """
        添加一个字符串到SQL构建器中，并在前后添加空格。
        :param string: 要添加的字符串
        """
        if string:
            self.remove_last_blank()
            self.string_builder.append(f" {string} ")
        return self

    def append_string_with_symbol(self, string: str, symbol: Symbol):
        """
        添加一个带有符号（如括号、引号）的字符串到SQL构建器中。
        :param string: 要添加的字符串
        :param symbol: 符号，包括单引号、双引号、括号或重音符
        """
        if not string and symbol == Symbol.ACCENT:
            return self

        if string is None:
            string = ""

        self.remove_last_blank()
        close = Symbol.CLOSE_PAREN if symbol == Symbol.OPEN_PAREN else symbol
        self.string_builder.append(f" {symbol}{string}{close} ")

        return self

    def append_long(self, long: int):
        """
        添加一个长整数到SQL构建器中，并在前后添加空格。
        :param long: 要添加的长整数
        """
        if long is not None:
            self.remove_last_blank()
            self.string_builder.append(f" {long} ")
        return self

    def append_long_with_paren(self, long: int):
        """
        添加一个带有括号的长整数到SQL构建器中。
        :param long: 要添加的长整数
        """
        if long is not None:
            self.remove_last_blank()
            self.string_builder.append(f" ({long}) ")
        return self

    def append_operator(self, operator_type: OperatorType):
        """
        添加一个操作符到SQL构建器中，并在前后添加空格。
        :param operator_type: 要添加的操作符
        """
        if OperatorType:
            self.remove_last_blank()
            self.string_builder.append(f" {operator_type.code} ")
        return self

    def append_relation(self, relation: Relation):
        """
        添加一个关系符到SQL构建器中，并在前后添加空格。
        :param relation: 要添加的关系符
        """
        if relation:
            self.remove_last_blank()
            self.string_builder.append(f" {relation.code} ")
        return self

    def append_symbol(self, symbol: Symbol):
        """
        添加一个符号到SQL构建器中，并根据符号类型添加适当的空格。
        :param symbol: 要添加的符号
        """
        if symbol:
            if symbol in [Symbol.OPEN_PAREN, Symbol.PLACE_HOLDER]:
                self.string_builder.append(" ")
            self.string_builder.append(symbol.code)
            if symbol in [Symbol.CLOSE_PAREN, Symbol.COMMA, Symbol.PLACE_HOLDER]:
                self.string_builder.append(" ")
        return self

    def append_table(self, table: Table):
        """
        添加一个表名到SQL构建器中，可选地包含别名。
        :param table: 要添加的表名
        """
        if table.name:
            self.remove_last_blank()
            self.append_string(table.fully_name)
        return self

    def append_column(self, column: Column, has_table_name: bool, has_alias: bool):
        """
        添加一个列名到SQL构建器中，可选地包含表名和别名。
        :param column: 要添加的列名
        :param has_table_name: 是否包含表名
        :param has_alias: 是否包含别名
        """
        if not column.is_empty:
            self.remove_last_blank()
            self.append_string(column.get_whole_name(has_table_name, has_alias))
        return self

    def append_without_paren(self, columns: List[Column], has_table_name: bool):
        """
        添加一个列的列表到SQL构建器中，不包含括号。
        :param columns: 要添加的列的列表
        :param has_table_name: 是否包含表名
        """
        if not columns:
            return self
        for i, column in enumerate(columns):
            if i > 0:
                self.append_symbol(Symbol.COMMA)
            self.append_column(column, has_table_name, False)
        return self

    def append_with_paren(self, columns: List[Column], has_table_name: bool):
        """
        添加一个列的列表到SQL构建器中，并在前后添加括号。
        :param columns: 要添加的列的列表
        :param has_table_name: 是否包含表名
        """
        if not columns:
            return self
        self.append_symbol(Symbol.OPEN_PAREN)
        self.append_without_paren(columns, has_table_name)
        self.append_symbol(Symbol.CLOSE_PAREN)
        return self

    def append_symbol_with_paren(self, symbol: Symbol, param_count: int):
        """
        添加多个符号到SQL构建器中，并用括号包含。
        :param symbol: 要添加的符号
        :param param_count: 符号的个数
        """
        if param_count > 0:
            self.append_symbol(Symbol.OPEN_PAREN)
            for i in range(param_count):
                if i > 0:
                    self.append_symbol(Symbol.COMMA)
                self.append_symbol(symbol)
            self.append_symbol(Symbol.CLOSE_PAREN)
        return self

    def clear(self):
        """
        清空SQL构建器。
        """
        self.string_builder = []

    @property
    def size(self) -> int:
        """
        获取SQL构建器的大小。
        :return: SQL构建器的大小
        """
        return len(self.string_builder)

    @property
    def is_empty(self) -> bool:
        """
        检查SQL构建器是否为空。
        :return: 如果为空则返回True，否则返回False
        """
        return len(self.string_builder) == 0

    def __str__(self) -> str:
        """
        将SQL构建器转换为字符串。
        :return: SQL构建器的字符串表示
        """
        return " ".join(self.string_builder).replace("  ", " ")

    def is_at_end(self, keyword: str) -> bool:
        """
        检查一个关键字是否在SQL构建器的末尾。
        :param keyword: 要检查的关键字
        :return: 如果关键字在末尾则返回True，否则返回False
        """
        return not self.is_empty and self.string_builder[-1].endswith(keyword)

    def remove_last_char(self):
        """
        移除SQL构建器中的最后一个字符。
        """
        self.string_builder[-1] = self.string_builder[-1][:-1]

    def remove_last_keyword(self, keyword: str):
        """
        移除SQL构建器中的最后一个关键字。
        :param keyword: 要移除的关键字
        """
        if keyword:
            idx_last = "".join(self.string_builder).rfind(keyword)
            if idx_last > 0:
                self.string_builder = self.string_builder[:idx_last] + self.string_builder[idx_last + len(keyword):]

    def remove_last_blank(self):
        """
        移除SQL构建器中的最后一个空格。
        """
        if self.string_builder and self.string_builder[-1].endswith(" "):
            self.string_builder[-1] = self.string_builder[-1][:-1]

    def remove_first_type(self, first_type: OperatorType):
        """
        移除SQL构建器中第一个出现的类型。
        :param first_type: 要移除的类型
        """
        if first_type:
            idx_first = "".join(self.string_builder).find(first_type.code)
            if idx_first > 0:
                self.string_builder = self.string_builder[:idx_first] + self.string_builder[
                                                                        idx_first + len(first_type.code):]