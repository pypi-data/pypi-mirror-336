import sqlparse
from mag_tools.exception.dao_exception import DaoException
from mag_tools.utils.common.string_utils import StringUtils
from sqlparse.sql import Comparison, Statement, Token

from mag_db.bean.column import Column
from mag_db.bean.table_info import TableInfo
from mag_db.parser.base_parser import BaseParser
from mag_db.utils.column_utils import ColumnUtils


class UpdateParser(BaseParser):
    def _parse(self, stmt: Statement) -> TableInfo:
        # 提取表名及别名
        tables = super()._find_table(stmt, {'UPDATE'})

        # 将SQL语句中”表别名.列名“转为”表名.列名“
        sql = ColumnUtils.convert_column_name(stmt.value, tables)
        stmt = sqlparse.parse(sql)[0]

        # 提取列名及其数值
        columns_token = self.__find_column_name_token(stmt)
        columns, values = self.__parse_column(columns_token)

        # 提取条件部分
        where = super()._find_where(stmt)

        return TableInfo(tables, columns, values=values, where=where)

    @classmethod
    def __find_column_name_token(cls, stmt: Statement):
        column_name_token = None
        set_token = super()._find_keyword(stmt, "SET")
        if set_token:
            column_name_token = super()._next_token(stmt, set_token)

        if not column_name_token or not isinstance(column_name_token, Token) or column_name_token.ttype is not None:
            raise DaoException(f"SQL解析错误，找不到列名:{stmt.value}")

        return column_name_token

    @classmethod
    def __parse_column(cls, columns_token: Token):
        columns = []
        values = []
        for token in columns_token.tokens:
            if isinstance(token, Comparison):
                column_name = StringUtils.pick_head(token.value, '=')
                column_value = StringUtils.pick_tail(token.value, '=')
                columns.append(Column(column_name))
                values.append(column_value)
        return columns, values

if __name__ == "__main__":
    # 示例用法
    _sql = "UPDATE table_name1 AS t SET t.column1 = 'value1', t.column2 = 'value2' WHERE id = 1;"

    _stmt = sqlparse.parse(_sql)[0]
    _result = UpdateParser(_stmt)
    if _result.table_info:
        print(_result.table_info)
