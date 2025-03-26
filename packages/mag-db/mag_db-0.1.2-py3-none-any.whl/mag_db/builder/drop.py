from mag_db.builder.base_sql import BaseSql
from mag_db.model.operator_type import OperatorType


class Drop(BaseSql):
    """
    Drop语句操作类

    @description: 用于构建DROP语句。
    @version: v1.0
    @date: 2019/8/30
    """
    def __init__(self, table_name: str):
        """
        构造方法

        :param table_name: 表名
        """
        super().__init__()

        self.append_operator(OperatorType.DROP_TABLE).append_string(table_name)