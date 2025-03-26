from dataclasses import dataclass
from typing import List

@dataclass
class ForeignKey:
    """
    描述一个外键约束

    属性:
    column_names (List[str]): 外键列名列表
    referenced_table (str): 引用的表名
    referenced_columns (List[str]): 引用的列名列表
    """
    column_names: List[str]  # 外键列名列表
    referenced_table: str  # 引用的表名
    referenced_columns: List[str]  # 引用的列名列表

    def __str__(self):
        """
        返回外键约束的字符串表示

        返回:
        str: 外键约束的字符串表示
        """
        column_names_str = ', '.join(self.column_names)
        referenced_columns_str = ', '.join(self.referenced_columns)
        return f"FOREIGN KEY ({column_names_str}) REFERENCES {self.referenced_table}({referenced_columns_str})"