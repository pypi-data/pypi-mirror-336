from typing import List, Optional

from mag_tools.model.symbol import Symbol

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.builder.sql_builder import SqlBuilder
from mag_db.builder.where import Where
from mag_db.model.operator_type import OperatorType
from mag_db.model.relation import Relation
from mag_db.model.sql_type import SqlType
from mag_db.parser.sql_parser import SqlParser


class BaseSql:
    def __init__(self, sql: Optional[str] = None):
        self.builder = SqlBuilder()
        self.tables = SqlParser(sql).tables

    def append_operator(self, operator_type:OperatorType):
        self.builder.append_operator(operator_type)
        return self

    def append_symbol(self, symbol:Symbol):
        self.builder.append_symbol(symbol)
        return self

    def append_string(self, string:str):
        self.builder.append_string(string)
        return self

    def append_string_with_symbol(self, string: str, symbol: Symbol):
        self.builder.append_string_with_symbol(string, symbol)
        return self

    def append_long(self, long: int):
        self.builder.append_long(long)
        return self

    def append_long_with_paren(self, long: int):
        self.builder.append_long_with_paren(long)
        return self

    def remove_last_char(self):
        self.builder.remove_last_char()
        return self

    def remove_last_keyword(self, keyword: str):
        self.builder.remove_last_keyword(keyword)
        return self

    def append_relation(self, relation: Relation):
        self.builder.append_relation(relation)
        return self

    def append_with_paren(self, columns: List[Column], is_multiple_table: bool):
        self.builder.append_with_paren(columns, is_multiple_table)
        return self

    def append_comment(self, comment: str):
        self.builder.append_string_with_symbol(comment, Symbol.SINGLE_QUOTATION)
        return self

    def clear(self):
        self.builder.clear()

    def get_param_count(self):
        return self.builder.__str__().count(Symbol.PLACE_HOLDER.code)

    def __str__(self):
        return self.builder.__str__()

    def append_tables(self, tables: List[Table]):
        self.tables = tables

        for i, table in enumerate(tables):
            if i > 0:
                self.builder.append_symbol(Symbol.COMMA)
            self.builder.append_table(table)

        return self

    def append_column(self, column: Column, has_table_name: bool, has_alias: bool):
        self.builder.append_column(column, has_table_name, has_alias)
        return self

    def append_whole_columns(self, columns: List[Column]):
        for column in columns:
            self.append_whole_column(column)

    def append_simple_columns(self, columns: List[Column]):
        for column in columns:
            self.append_column(column, False, False).append_symbol(Symbol.COMMA)

    def append_condition(self, where: Where):
        if where:
            self.builder.append_string(str(where))
        return self

    def replace(self, old_chars: str, new_chars: str):
        self.builder = SqlBuilder(self.builder.__str__().replace(old_chars, new_chars))

    @classmethod
    def to_columns(cls, column_names: List[str]) -> List[Column]:
        return [Column(name[:-1] if name.endswith('_') else name) for name in column_names]

    def append_whole_column(self, column: Column):
        self.append_string(column.name)

        sql_type = column.sql_type
        if sql_type:
            self.append_string(sql_type.code)

            if sql_type in [SqlType.CHAR, SqlType.VARCHAR]:
                column_size = column.column_size or 255

                if column.masking_alg and (column.masking_alg.is_hash() or column.masking_alg.is_crypt()):
                    if sql_type == SqlType.CHAR:
                        if column_size < 255 - 32:
                            column_size = 255
                        else:
                            column_size += 128
                            sql_type = SqlType.VARCHAR
                    else:
                        column_size += 128

                self.append_long_with_paren(column_size)
            elif sql_type == SqlType.BIT:
                column_size = column.column_size or 64
                self.append_long_with_paren(column_size)
            elif sql_type == SqlType.VARBINARY:
                column_size = column.column_size or 1024
                self.append_long_with_paren(column_size)
            elif sql_type in [SqlType.DATETIME, SqlType.TIMESTAMP]:
                decimal_digits = column.decimal_digits
                if decimal_digits and decimal_digits > 0:
                    self.append_long_with_paren(decimal_digits)
            elif sql_type in [SqlType.TINYINT, SqlType.INT]:
                if column.is_zero_filling:
                    self.append_long_with_paren(10)
                if column.is_unsigned:
                    self.append_operator(OperatorType.UNSIGNED)
            elif sql_type in [SqlType.DECIMAL, SqlType.DOUBLE, SqlType.FLOAT]:
                if column.column_size and column.decimal_digits:
                    self.builder.append_symbol(Symbol.OPEN_PAREN)
                    self.append_long(column.column_size)
                    self.builder.append_symbol(Symbol.COMMA)
                    self.append_long(column.decimal_digits)
                    self.builder.append_symbol(Symbol.CLOSE_PAREN)
            elif sql_type == SqlType.ENUM:
                self.builder.append_symbol(Symbol.OPEN_PAREN)
                self.append_string_with_symbol(column.enum_values, Symbol.SINGLE_QUOTATION)
                self.builder.append_symbol(Symbol.CLOSE_PAREN)

        self.append_string(OperatorType.NULL.code if column.is_can_null else OperatorType.NOT_NULL.code)

        if column.is_auto_increment:
            self.append_string(OperatorType.AUTO_INCREMENT.name)

        default_value = column.default_value
        if default_value:
            self.append_operator(OperatorType.DEFAULT)

            if "CURRENT_TIMESTAMP" in default_value.upper():
                if not column.decimal_digits:
                    idx = default_value.find("(")
                    if idx > 0:
                        default_value = default_value[:idx]
                self.append_string(default_value)
            elif sql_type == SqlType.BIT:
                default_value = default_value.replace("b", "").replace("'", "")
                self.append_string(default_value)
            else:
                self.append_string_with_symbol(default_value, Symbol.SINGLE_QUOTATION)
        else:
            if not column.is_primary_key and column.is_can_null:
                self.append_string(OperatorType.DEFAULT.code).append_operator(OperatorType.NULL)

        if column.comment:
            self.append_operator(OperatorType.COMMENT).append_comment(column.comment)
        self.builder.append_symbol(Symbol.COMMA)
