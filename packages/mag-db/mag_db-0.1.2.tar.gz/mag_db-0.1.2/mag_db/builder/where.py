from typing import Any, List

from mag_tools.model.base_enum import BaseEnum
from mag_tools.model.symbol import Symbol
from mag_tools.utils.common.string_utils import StringUtils

from mag_db.bean.column import Column
from mag_db.bean.db_page import DbPage
from mag_db.builder.sql_builder import SqlBuilder
from mag_db.model.operator_type import OperatorType
from mag_db.model.relation import Relation


class Where:
    """
    WHERE语句操作类

    @description: 用于构建WHERE语句。
    @author <a href="xl.cao@hotmail.com">xlcao</a>
    @version v1.1
    Copyright (c) 2016 by Xiaolong Cao. All rights reserved.
    @date: 2017/8/12
    """
    def __init__(self, sql: str = None):
        """
        构造方法
        """
        self.builder = SqlBuilder()
        self.fields = []
        self.is_page_query = False
        self.page = None

        if sql:
            if sql.upper().startswith('WHERE'):
                sql = StringUtils.pick_tail(sql, ' ')

            self.builder.append_string(sql)

    @staticmethod
    def builder():
        """
        构造方法
        """
        return Where()

    def and_(self):
        """
        添加“AND”

        :return: Where
        """
        return self.append_type(OperatorType.AND)

    def or_(self):
        """
        添加“OR”

        :return: Where
        """
        return self.append_type(OperatorType.OR)

    def column(self, column_name: str, relation: Relation, value: Any, ignore_null_value: bool = True):
        """
        添加列参数

        :param column_name: 列名
        :param relation: 列名与参数的关系类型，大于、小于、等于、不小于、不大于、不等于、LIKE、NOT LIKE等
        :param value: 列值
        :param ignore_null_value: 是否忽略空值
        :return: Where
        """
        if isinstance(relation, str):
            relation = Relation.of_code(relation)

        if (column_name and
                (not ignore_null_value or value is not None) and
                relation in [Relation.MORE_THAN, Relation.MORE_THAN_EQUAL, Relation.LESS_THAN, Relation.LESS_THAN_EQUAL, Relation.EQUAL, Relation.NOT_EQUAL, Relation.LIKE, Relation.NOT_LIKE]):
            if self.builder.is_empty:
                self.builder.append_operator(OperatorType.WHERE)
            has_table_name = "." in column_name
            self.builder.append_column(Column(name=column_name), has_table_name, False).append_relation(relation).append_symbol(Symbol.PLACE_HOLDER)
            self.add_field(value)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def column_value(self, column_name: str, value: Any, ignore_null_value: bool = True):
        """
        添加列参数

        :param column_name: 列名
        :param value: 列值
        :param ignore_null_value: 是否忽略空值
        :return: Where
        """
        if column_name and (not ignore_null_value or value is not None):
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE)
            self.column(column_name, Relation.EQUAL, value)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def equal_column(self, column1: str, column2: str):
        """
        添加指定列等于另外一列

        :param column1: 列名
        :param column2: 列名
        :return: Where
        """
        if column1 and column2:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE)
            self.builder.append_column(Column(name=column1), True, False).append_relation(Relation.EQUAL).append_column(Column(name=column2), True, False)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def in_select_str(self, column: str, select_str: str):
        """
        添加“IN”条件
        WHERE ... AND/OR column IN (SELECT语句)

        :param column: 列名
        :param select_str: IN的查询条件，SELECT * FROM WHERE *
        :return: Where
        """
        if column and select_str:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.IN)
            self.append_paren(select_str)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def in_select(self, column: str, select):
        """
        添加“IN”条件
        WHERE ... AND/OR column IN (SELECT语句)

        :param column: 列名
        :param select: IN的查询条件，SELECT * FROM WHERE *
        :return: Where
        """
        if column and select:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.IN)
            self.append_paren(str(select))
            if select.get_where():
                self.fields.extend(select.get_where().fields)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def in_list(self, column: str, params: List[Any]):
        """
        添加“IN”条件
        WHERE... column IN (str1, str2...)

        :param column: 列名
        :param params: IN的参数列表
        :return: Where
        """
        if column and params:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.IN)
            param_strs = [f"'{param}'" if isinstance(param, str) else str(param) for param in params]
            in_str = ", ".join(param_strs)
            self.append_paren(in_str)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def not_in_list(self, column: str, params: List[Any]):
        """
        添加“NOT IN”条件
        WHERE... column NOT IN (str1, str2...)

        :param column: 列名
        :param params: NOT IN的参数列表
        :return: Where
        """
        if column and params:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.NOT_IN)
            param_strs = [f"'{param}'" if isinstance(param, str) else str(param) for param in params]
            not_in_str = ", ".join(param_strs)
            self.append_paren(not_in_str)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def in_place_holder(self, column_name: str, param_count: int):
        """
        添加“IN”条件
        WHERE... column IN (?, ?...)

        :param column_name: 列名
        :param param_count: IN的参数个数
        :return: Where
        """
        if column_name and param_count > 0:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column_name), True, False).append_operator(OperatorType.IN)
            self.builder.append_symbol_with_paren(Symbol.PLACE_HOLDER, param_count)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def in_fields(self, column: str, fields: List[Any]):
        """
        添加“IN”条件
        WHERE... column IN (?, ?...)

        :param column: 列名
        :param fields: IN的参数列表
        :return: Where
        """
        self.in_place_holder(column, len(fields))
        self.add_fields(fields)
        return self

    def not_in(self, column: str, param_count: int):
        """
        添加“NOT IN”条件
        WHERE... column NOT IN (?, ?...)

        :param column: 列名
        :param param_count: NOT IN的参数个数
        :return: Where
        """
        if column and param_count > 0:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.NOT_IN)
            self.builder.append_symbol_with_paren(Symbol.PLACE_HOLDER, param_count)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def not_in_fields(self, column: str, fields: List[Any]):
        """
        添加“NOT IN”条件
        WHERE... column NOT IN (?, ?...)

        :param column: 列名
        :param fields: NOT IN的参数列表
        :return: Where
        """
        self.not_in(column, len(fields))
        self.add_fields(fields)
        return self

    def not_in_select_str(self, column: str, select_str: str):
        """
        添加“NOT IN”条件
        WHERE... column NOT IN (SELECT语句)

        :param column: 列名
        :param select_str: NOT IN的查询条件，SELECT * FROM WHERE *
        :return: Where
        """
        if column and select_str:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.NOT_IN.code)
            self.append_paren(select_str)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def not_in_select(self, column: str, select):
        """
        添加“NOT IN”条件
        WHERE... column NOT IN (SELECT语句)

        :param column: 列名
        :param select: NOT IN的查询条件，SELECT * FROM WHERE *
        :return: Where
        """
        if column and select:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE.code)
            self.builder.append_column(Column(name=column), True, False).append_operator(OperatorType.NOT_IN)
            self.append_paren(str(select))
            if select.where:
                self.fields.extend(select.where.fields)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def order(self, ascend: bool, *column_names: str):
        """
        添加“ORDER”条件
        ORDER (col1, col2)

        :param ascend: 是否升序
        :param column_names: 列名列表
        :return: Where
        """
        if column_names:
            has_table_name = "." in column_names[0]
            self.builder.append_operator(OperatorType.ORDER_BY)

            columns = [Column(name[:-1] if name.endswith('_') else name) for name in column_names]
            self.builder.append_without_paren(columns, has_table_name)
            if not ascend:
                self.builder.append_operator(OperatorType.DESC)
        return self

    def like(self, column: str, value: str):
        """
        添加LIKE条件

        :param column: 列名
        :param value: 列值
        :return: Where
        """
        if column and value:
            if not value.startswith("%") and not value.endswith("%"):
                value = f"%{value}%"
            self.column(column, Relation.LIKE, value)
        else:
            if self.builder.is_at_end(OperatorType.AND.code):
                self.builder.remove_last_keyword(OperatorType.AND.code)
            elif self.builder.is_at_end(OperatorType.OR.code):
                self.builder.remove_last_keyword(OperatorType.OR.code)
        return self

    def sub_query(self, relation: str, column: str, sub_query: str):
        """
        添加子查询

        :param relation: 列名与参数的关系类型，大于、小于、等于、不小于、不大于、不等于、LIKE、NOT LIKE等
        :param column: 列名
        :param sub_query: 查询子语句
        :return: Where
        """
        if sub_query and relation in [Relation.MORE_THAN, Relation.MORE_THAN_EQUAL, Relation.LESS_THAN, Relation.LESS_THAN_EQUAL, Relation.EQUAL, Relation.NOT_EQUAL, Relation.LIKE, Relation.NOT_LIKE]:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE)
            self.builder.append_column(Column(name=column), True, False).append_relation(relation)
            self.append_paren(sub_query)
        return self

    def sub_where(self, sub_where):
        """
        添加子语句

        :param sub_where: 子条件语句，不包含WHERE
        :return: Where
        """
        if sub_where:
            if self.builder.is_empty:
                self.append_type(OperatorType.WHERE)
            if sub_where.builder.sql.startswith(OperatorType.WHERE.code):
                sub_where.builder.sql = sub_where.builder.sql[5:]
            self.builder.append_symbol(Symbol.OPEN_PAREN)
            self.builder.append_string(sub_where.builder.sql)
            self.builder.append_symbol(Symbol.CLOSE_PAREN)
            self.fields.extend(sub_where.fields)
        return self

    def limit(self, offset: int = None, row_count: int = None):
        """
        添加LIMIT条件

        :param offset: 记录行数偏移量
        :param row_count: 最大记录数
        :return: Where
        """
        if row_count is not None:
            self.builder.append_operator(OperatorType.LIMIT)
            if offset is not None:
                self.builder.append_long(offset).append_symbol(Symbol.COMMA)
            self.builder.append_long(row_count)
        return self

    def group_by(self, sql_group: str):
        """
        添加GROUP BY条件

        :param sql_group: Group语句
        :return: Where
        """
        if sql_group:
            self.builder.append_operator(OperatorType.GROUP_BY).append_string(sql_group)
        return self

    def for_update(self):
        """
        添加FOR UPDATE条件

        :return: Where
        """
        self.builder.append_operator(OperatorType.FOR_UPDATE)
        return self

    def __str__(self):
        """
        流化为SQL语句

        :return: SQL语句
        """
        sql = self.builder.__str__().strip()
        if not sql.startswith(OperatorType.WHERE.code) and not any(sql.startswith(keyword) for keyword in [OperatorType.GROUP.code, OperatorType.ORDER.code, OperatorType.LIMIT.code]):
            sql = f"{OperatorType.WHERE.code} {sql}"
        return sql if len(sql) >= 8 else ""

    def append_paren(self, *sql_strs: str):
        """
        添加括号包含起来的字符串,如：(语句1，语句2...)

        :param sql_strs: SQL语句
        """
        if sql_strs:
            self.builder.append_symbol(Symbol.OPEN_PAREN)
            for sql_str in sql_strs:
                if sql_str:
                    self.builder.append_string(sql_str)
            self.builder.append_symbol(Symbol.CLOSE_PAREN)

    def set_params(self, params: List[str]):
        """
        将条件语句中的多个问号替换为字符串参数

        :param params: 参数列表
        :return: Where
        """
        sql = str(self)
        for param in params:
            sql = sql.replace(Symbol.PLACE_HOLDER.code, f"'{param}'", 1)
        return Where(sql)

    def has_fields(self):
        """
        判定是否包含条件参数的值

        :return: 是否包含条件参数的值
        """
        return bool(self.fields)

    def page(self, page):
        """
        设置分页查询参数

        :param page: 页面信息，包括：页面索引，从1开始；页面大小
        :return: Where
        """
        self.page = page or DbPage(1, 10)
        self.is_page_query = True
        if self.page.order_column:
            self.order(self.page.is_ascend, self.page.order_column)
        if self.builder.is_at_end("AND"):
            self.builder.remove_last_keyword("AND")
        elif self.builder.is_at_end("OR"):
            self.builder.remove_last_keyword("OR")
        return self

    @property
    def is_empty(self):
        """
        判定是否为空

        :return: 是否为空
        """
        return self.builder.is_empty

    def add_fields(self, fields: List[Any]):
        """
        添加条件参数的值（替代问号）

        :param fields: 条件参数的值
        """
        if fields:
            for field in fields:
                self.add_field(field)

    def append_type(self, operator_type: OperatorType):
        """
        添加“AND”、“OR”、“IN”、“NOT IN”

        :param operator_type: 操作符类型
        :return: Where
        """
        if isinstance(operator_type, str):
            operator_type = OperatorType.of_code(operator_type)

        last = StringUtils.last_word(self.builder.__str__().strip()).upper()
        if self.builder.is_empty and operator_type in [OperatorType.AND, OperatorType.OR]:
            return self
        if last not in [OperatorType.WHERE, OperatorType.AND, OperatorType.OR, OperatorType.IN, OperatorType.NOT_IN, OperatorType.GROUP_BY, OperatorType.ORDER_BY]:
            self.builder.append_operator(operator_type)
        return self

    def add_field(self, value: Any):
        """
        添加条件参数值，对枚举添加其value值

        :param value: 条件参数值
        """
        self.fields.append(value.code if isinstance(value, BaseEnum) else value)