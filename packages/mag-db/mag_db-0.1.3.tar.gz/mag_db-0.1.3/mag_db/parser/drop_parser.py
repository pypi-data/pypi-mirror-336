import sqlparse
from sqlparse.sql import Statement

from mag_db.bean.table_info import TableInfo
from mag_db.parser.base_parser import BaseParser


class DropParser(BaseParser):
    def _parse(self, stmt: Statement) -> TableInfo:
        # 提取表名
        tables = super()._find_table(stmt, {'EXISTS', 'TABLE'})
        return TableInfo(tables)


if __name__ == "__main__":
    # 示例用法
    _sql = "DROP TABLE IF EXISTS table_name1;"

    _stmt = sqlparse.parse(_sql)[0]
    parser = DropParser(_stmt)
    if parser.table_info:
        print(parser.table_info)
