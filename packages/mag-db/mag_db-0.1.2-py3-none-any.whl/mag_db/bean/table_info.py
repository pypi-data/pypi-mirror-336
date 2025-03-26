from typing import Any, Dict, List, Optional

from mag_db.bean.foreign_key import ForeignKey
from mag_db.bean.primary_key import PrimaryKey
from mag_db.bean.column import Column
from mag_db.bean.table import Table


class TableInfo:
    def __init__(self, tables: List[Table], columns: List[Column] = [], primary_key: Optional[PrimaryKey] = None,
                 foreign_keys: List[ForeignKey] = [], distinct: bool = False, values: Optional[List[Any]] = None,
                 where : Optional[str] = None, group_by:Optional[str] = None, having: Optional[str] = None,
                 order_by:Optional[str]= None, charset: Optional[str] = None, engine: Optional[str] = None,
                 comment: Optional[str] = None, column_name_map: Optional[Dict[str, str]] = None, auto_increment: bool= False) -> None:
        self.tables = tables
        self.columns = columns
        self.__primary_key = primary_key
        self.foreign_keys = foreign_keys
        self.values = values
        self.distinct = distinct
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by
        self.charset = charset
        self.engine = engine
        self.comment = comment
        self.auto_increment = auto_increment

        self.column_name_map = column_name_map
        if not self.column_name_map:
            self.column_name_map = TableInfo.__get_column_name_map(columns)

    @property
    def table_names(self) -> List[str]:
        return [table.name for table in self.tables]

    def get_column_names(self, is_query: bool = False) -> List[str]:
        column_names = [column.name for column in self.columns]

        # 对于非查询类操作，如主键是自增型，则排除
        if not is_query and self.auto_increment and self.__primary_key:
            column_names.remove(self.__primary_key.default_column)

        return column_names

    @property
    def default_primary_key(self) -> Optional[str]:
        return self.__primary_key.default_column if self.__primary_key else None

    def __str__(self):
        foreign_keys_str_list = [foreign_key.__str__() for foreign_key in self.foreign_keys]

        parts = [ f"tables=[{', '.join(self.table_names)}]",
                  f"columns=[{', '.join(self.get_column_names())}]" if self.columns else "",
                  f"primary_key={self.__primary_key}" if self.__primary_key else "",
                  f"foreign_keys=[{', '.join(foreign_keys_str_list)}]" if len(self.foreign_keys) > 0 else "",
                  f"distinct={self.distinct}",
                  f"values={self.values}" if self.values else "",
                  f"where={self.where}" if self.where else "",
                  f"group_by={self.group_by}" if self.group_by else "",
                  f"having={self.having}" if self.having else "",
                  f"order_by={self.order_by}" if self.order_by else "",
                  f"column_name_map={self.column_name_map}" if self.column_name_map else ""
        ]
        # 过滤掉空字符串
        parts = [part for part in parts if part]
        return f"TableInfo({', '.join(parts)})"

    @classmethod
    def __get_column_name_map(cls, columns: List[Column]) -> Dict[str, str]:
        mappings = {}
        for column in columns:
            map_value = column.mapping
            if map_value:
                mappings[column.name] = map_value
        return mappings
