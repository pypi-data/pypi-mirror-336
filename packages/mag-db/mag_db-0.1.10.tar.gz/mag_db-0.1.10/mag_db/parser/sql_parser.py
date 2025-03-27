from typing import List, Optional

import sqlparse

from mag_db.bean.table_info import TableInfo
from mag_db.parser.create_parser import CreateParser
from mag_db.parser.delete_parser import DeleteParser
from mag_db.parser.drop_parser import DropParser
from mag_db.parser.insert_parser import InsertParser
from mag_db.parser.query_parser import QueryParser
from mag_db.parser.update_parser import UpdateParser


class SqlParser:
    def __init__(self, sql: str):
        parser = None

        if sql:
            stmt = sqlparse.parse(sql)[0]

            if stmt.get_type() == 'SELECT':
                parser = QueryParser(stmt)
            elif stmt.get_type() == 'UPDATE':
                parser = UpdateParser(stmt)
            elif stmt.get_type() == 'INSERT':
                parser = InsertParser(stmt)
            elif stmt.get_type() == 'DELETE':
                parser = DeleteParser(stmt)
            elif stmt.get_type() == 'DROP':
                parser = DropParser(stmt)
            elif stmt.get_type() == 'CREATE':
                parser = CreateParser(stmt)

        self.sql = sql
        self.__table_info = parser.table_info if parser else TableInfo([])

    @property
    def tables(self):
        return self.__table_info.tables

    @property
    def table_names(self) -> List[str]:
        return self.__table_info.table_names

    def column_names(self, is_query: bool = False) -> List[str]:
        return self.__table_info.get_column_names(is_query)

    @property
    def default_primary_key(self) -> Optional[str]:
        return self.__table_info.default_primary_key
