from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PrimaryKey:
    """
    描述一个主键约束

    属性:
    column_names (List[str]): 主键列名列表
    key_seq (Optional[List[int]]): 主键列的顺序列表，默认为 None
    pk_name (Optional[str]): 主键的名称，默认为 None
    increment (Optional[int]): 自增列的增量值，默认为 None
    """
    column_names: List[str] = field(default_factory=list) # 主键列名列表
    key_seq: List[int] = field(default_factory=list)  # 主键列的顺序列表，默认为 None
    pk_name: Optional[str] = None  # 主键的名称，默认为 None
    increment: Optional[int] = None  # 自增列的增量值，默认为 None

    @property
    def default_column(self) -> str:
        return self.column_names[0] if self.column_names and len(self.column_names) == 1 else None

    def __str__(self):
        """
        返回主键约束的字符串表示

        返回:
        str: 主键约束的字符串表示
        """
        parts = [f"PRIMARY KEY ({', '.join(self.column_names)})"]
        if self.key_seq and len(self.key_seq) > 0:
            parts.append(f"KEY_SEQ ({', '.join(map(str, self.key_seq))})")
        if self.pk_name:
            parts.append(f"PK_NAME {self.pk_name}")
        if self.increment:
            parts.append(f"INCREMENT {self.increment}")
        return " ".join(parts)