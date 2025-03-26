import sqlparse
from mag_tools.exception.dao_exception import DaoException
from mag_tools.utils.common.string_utils import StringUtils
from sqlparse.sql import Statement

from mag_db.bean.table import Table
from mag_db.bean.table_info import TableInfo
from mag_db.parser.base_parser import BaseParser


class InsertParser(BaseParser):
    def _parse(self, stmt: Statement) -> TableInfo:
        # 提取表名/表别名、列名/列别名
        table_name_token = super()._find_keyword(stmt, 'INTO')
        table_full_name = super()._get_value_of_token(stmt, table_name_token)  # 包含列名
        table_name, column_names_str, _ = StringUtils.split_by_keyword(table_full_name, '()')

        # 提取表名
        if not table_name:
            raise DaoException(f'表名不存在:{stmt.value}')

        tables = [Table(table_name)]

        # 提取列名及其别名
        columns = super()._parse_column_names(column_names_str)

        # 提取值
        values_token = super()._find_values(stmt)
        values = [token.value for token in values_token.tokens if token.ttype is None]

        return TableInfo(tables, columns, values=values)

if __name__ == '__main__':
    # 示例用法
    _sql = "INSERT INTO table_name1 (column1, column2) VALUES ('value1', 'value2');"

    _stmt = sqlparse.parse(_sql)[0]
    _parser = InsertParser(_stmt)
    if _parser.table_info:
        print(_parser.table_info)
