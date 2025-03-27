from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.model.masking_alg import MaskingAlg

from mag_db.model.sql_type import SqlType


@dataclass
class Column:
    name: Optional[str] = None  # 列名
    sn: Optional[int] = None
    db_name: Optional[str] = None  # 库名
    table_name: Optional[str] = None  # 表名
    table_sn: Optional[int] = None  # 表序号
    alias: Optional[str] = name  # 别名
    mapping: Optional[str] = None   # 映射到Bean中的字段名
    sql_type: Optional[SqlType] = None  # 列的JDBC类型,比如：CHAR、TINYINT等
    is_unsigned: bool = False  # 是否为无符号数，在TINYINT、INT等有效
    is_zero_filling: bool = False  # 是否用零填充
    data_type: Optional[int] = None  # 数据类型
    is_primary_key: bool = False  # 是否为主键
    uniques: List[str] = field(default_factory=list)  # 是否唯一
    is_can_null: bool = True  # 可否为空
    column_size: Optional[int] = None  # 列大小
    decimal_digits: Optional[int] = None  # 小数位数
    num_prec_radix: Optional[int] = None  # 基数，通常为10或2
    char_octet_length: Optional[int] = None  # 字符类型长度，对char 类型，该长度是列中的最大字节数
    default_value: Optional[str] = None  # 列的缺省值
    ordinal_position: Optional[int] = None  # 列的原始位置
    is_auto_increment: bool = False  # 是否为自增主键
    enum_values: Optional[str] = None  # 枚举的可能值（类型为枚举时有效）
    masking_alg: Optional[MaskingAlg] = None  # 脱敏算法，包括掩码、加密、Hash
    _comment: Optional[str] = None  # 描述

    @classmethod
    def of_whole_name(cls, whole_col_name: Optional[str] = None):
        col = None
        if whole_col_name:
            # 分割表名和列名
            parts = whole_col_name.split(".", 1)
            table_name = parts[0] if len(parts) > 1 else None

            # 分割列名和别名
            parts = parts[-1].lower().split(" as ", 1)
            name = parts[0]
            _alias = parts[1] if len(parts) > 1 else None

            col = cls(name=name, table_name=table_name, alias=_alias, mapping=name)
        return col

    def get_whole_name(self, has_table_name=True, has_alias=True) -> str:
        """
        获取完整格式的列名，格式为：表名.列名 AS 列别名
        :param has_table_name: 是否包含表名
        :param has_alias: 是否包含别名
        :return: 完整格式的列名
        """
        if not self.name:
            return ""

        parts = []

        if has_table_name and self.table_name and not self.is_function:
            parts.append(f"{self.table_name}.")

        if not self.is_function and self.name != "*":
            parts.append(f"{self.name}")
        else:
            parts.append(self.name)

        if has_alias and self.alias:
            parts.append(f" AS {self.alias}")

        return "".join(parts)

    @property
    def short_name(self):
        """
        获取短格式列名，格式为：表名.列名
        :return: 短格式列名
        """
        return f"{self.table_name}.{self.name}" if self.table_name else self.name

    @property
    def is_function(self):
        """
        判定该列名是否为函数，函数名中包含有括号
        :return: 是否为函数
        """
        return self.name and "(" in self.name and ")" in self.name

    @property
    def is_empty(self):
        """
        判定列名是否为空
        :return: 是否为空
        """
        return not self.name

    @property
    def comment(self):
        """
        获取列的描述，去除特殊字符
        :return: 列的描述
        """
        if self._comment:
            self._comment = self._comment.replace("'", "").replace("\"", "")
        return self._comment

    @property
    def is_unique(self):
        """
        判定列是否唯一
        :return: 是否唯一
        """
        return len(self.uniques) > 0

    @classmethod
    def to_field_name(cls, column_name: str) -> str:
        column = cls(name=column_name)
        return column.name