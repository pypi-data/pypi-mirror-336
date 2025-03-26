from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from mag_db.bean.column import Column


@dataclass
class Table:
    name: Optional[str] = None  # 表名，不含别名
    sn: Optional[int] = None  # 表序号，主键
    schema_name: Optional[str] = None  # 表模式名
    table_type: str = "TABLE"  # 表类型名
    db_sn: Optional[int] = None  # 库序号
    db_name: Optional[str] = None  # 库名
    ds_name: Optional[str] = None  # 数据源名
    alias: Optional[str] = None  # 表别名
    primary_keys: str = ""  # 表的主键清单，逗号分开
    auto_increment: int = 0  # 自增长序号的起始值
    _columns: List[Column] = field(default_factory=list)  # 列名清单
    column_names_mapping: Dict[str, str] = field(default_factory=dict) # 列名与字段名映射表
    create_time: Optional[datetime] = None  # 创建时间
    comment: Optional[str] = None  # 描述

    @property
    def fully_name(self) -> str:
        """
        取完整表名
        """
        return f"{self.name} AS {self.alias}" if self.alias else self.name

    @property
    def columns(self) -> List[Column]:
        return self._columns

    def set_columns(self, columns: List[Column]):
        """
        设置列信息
        :param columns: 列信息清单
        """
        if columns:
            self._columns = columns

            # 设置表的主键：如添加列的信息中包含了是否为主键信息，则设置表的主键
            pri_keys = [col for col in self._columns if col.is_primary_key]
            if pri_keys:
                pri_key_strs = [col.name for col in pri_keys]
                self.primary_keys = ",".join(pri_key_strs)

    def set_column_names(self, column_names: List[str]):
        columns = [Column(name[:-1] if name.endswith('_') else name) for name in column_names]

        self.set_columns(columns)

    def set_sn(self, sn: int):
        """
        设置表序号
        :param sn: 表序号
        """
        self.sn = sn
        for col in self._columns:
            col.table_sn = sn

    def set_primary_keys(self, primary_keys: str):
        """
        设置表的主键信息
        :param primary_keys: 主键清单，逗号分开
        """
        if primary_keys:
            self.primary_keys = primary_keys

            # 更新列的主键信息
            pri_key_strs = primary_keys.split(",")
            for col in self._columns:
                if col.name in pri_key_strs:
                    col.is_primary_key = True

    def __str__(self) -> str:
        """
        流化为完整格式的字符串
        """
        return self.fully_name

    @property
    def uniques(self) -> List[Column]:
        """
        获取有唯一约束的列清单
        :return: 有唯一约束的列清单
        """
        return [col for col in self._columns if col.is_unique]

    def compare(self, table: 'Table') -> bool:
        """
        判定两个表是否相同
        :param table: 表信息
        :return: 是否相同
        """
        return str(self) == str(table)

    def add_column(self, column: Column):
        """
        添加列信息
        :param column: 列信息
        """
        self._columns.append(column)

        # 如该列为主键，但表主键列表中未包含，则添加为主键
        primary_key_strs = self.primary_keys.split(",")
        if column.is_primary_key and column.name not in primary_key_strs:
            primary_key_strs.append(column.name)
            self.primary_keys = ",".join(primary_key_strs)

    def check(self):
        """
        检查表信息格式
        """
        if not self._columns:
            self._columns = []
        if not self.primary_keys:
            self.primary_keys = ""
        if not self.table_type:
            self.table_type = "TABLE"

        for col in self._columns:
            if col.name in self.primary_keys:
                col.is_primary_key = True
                col.is_can_null = False
            col.table_name = self.name

    @classmethod
    def to_tables(cls, table_names: List[str]) -> List['Table']:
        """
        将表名列表转换为表的列表
        :param table_names: 表名的列表
        :return: 表的列表
        """
        return [Table(name=_name) for _name in table_names]