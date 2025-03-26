import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Punctuation

from mag_db.bean.column import Column
from mag_db.bean.table_info import TableInfo
from mag_db.parser.base_parser import BaseParser
from mag_db.utils.column_utils import ColumnUtils


class QueryParser(BaseParser):
    def _parse(self, stmt: Statement) -> TableInfo:
        # 提取表名、表别名
        tables = super()._find_table(stmt, {'FROM'})

        # 将SQL语句中”表别名.列名“转为”表名.列名“
        sql = ColumnUtils.convert_column_name(stmt.value, tables)
        stmt = sqlparse.parse(sql)[0]

        # 提取列名及其别名
        columns_token = super()._find_keyword(stmt, "SELECT")
        column_names_str = super()._get_value_of_token(stmt, columns_token)
        columns = super()._parse_column_names(column_names_str)

        # 提取条件部分
        where = super()._find_where(stmt)

        # 提取 GROUP BY 子句
        group_by = self.__group_by(stmt)
        having = self.__having(stmt)

        # 提取 ORDER BY 子句
        order_by = self.__order_by(stmt)

        return TableInfo(tables, columns, where=where, group_by=group_by, having=having, order_by=order_by)

    @classmethod
    def __parse_column_names(cls, columns_token: Token):
        columns = []
        for token in columns_token.tokens:
            if token.ttype is None:
                for part_token in token.tokens:
                    if part_token.ttype is None:
                        part_values = part_token.value.split()
                        if len(part_values) == 1:
                            column = Column(name=part_values[0])
                            columns.append(column)
                        elif len(part_values) == 3 and part_values[1].upper() == 'AS':
                            column = Column(name=part_values[0], alias=part_values[2])
                            columns.append(column)
        return columns

    @classmethod
    def __group_by(cls, stmt: Statement) -> [str]:
        # 提取 GROUP BY 子句
        group_by = []
        group_by_token = BaseParser._find_keyword(stmt, 'GROUP BY')
        if group_by_token:
            next_token = BaseParser._next_token(stmt, group_by_token)
            while next_token and not BaseParser._is_keyword(next_token.value):
                if next_token.ttype is not Punctuation:
                    group_by.append(next_token.value)

                next_token = BaseParser._next_token(stmt, next_token)
        return ' '.join(group_by) if group_by else None

    @classmethod
    def __having(cls, stmt: Statement) -> [str]:
        # 提取 HAVING 子句
        having_token = BaseParser._find_keyword(stmt, 'HAVING')
        having = []
        if having_token:
            next_token = BaseParser._next_token(stmt, having_token)
            while next_token and not BaseParser._is_keyword(next_token.value):
                having.append(next_token.value)
                next_token = BaseParser._next_token(stmt, next_token)
        return ' '.join(having) if len(having) > 0 else None

    @classmethod
    def __order_by(cls, stmt: Statement):
        # 提取 ORDER BY 子句
        order_by_token = BaseParser._find_keyword(stmt, 'ORDER BY')
        order_by = []
        if order_by_token:
            next_token = BaseParser._next_token(stmt, order_by_token)
            while next_token and not BaseParser._is_keyword(next_token.value):
                if next_token.ttype is not Punctuation:
                    order_by.append(next_token.value)

                next_token = QueryParser._next_token(stmt, next_token)
        return ' '.join(order_by) if len(order_by) > 0 else None


if __name__ == '__main__':
    # 示例用法
    _sql = "SELECT t.column1 AS c1, t.column2 AS c2 FROM table_name1 AS t WHERE t.id IN (1, 2, 3) AND t.name = 'John' GROUP BY t.column1 HAVING COUNT(t.column1) > 1 ORDER BY t.column2;"
    _stmt = sqlparse.parse(_sql)[0]
    _parser = QueryParser(_stmt)
    if _parser.table_info:
        print(_parser.table_info)
