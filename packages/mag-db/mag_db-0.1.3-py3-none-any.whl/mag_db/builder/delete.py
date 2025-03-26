from typing import List

from mag_db.bean.table import Table
from mag_db.builder.where import Where
from mag_db.builder.base_sql import BaseSql
from mag_db.model.operator_type import OperatorType


class Delete(BaseSql):
    """
    DELETE语句操作类

    @author: Xiaolong Cao
    @version: v1.0
    @description: 用于构建DELETE语句。
    @date: 2019/8/30
    """
    def __init__(self, table_names: List[str], where: Where = None):
        super().__init__()

        self.append_operator(OperatorType.DELETE) \
            .append_tables([Table(name) for name in table_names])

        if where is not None:
            self.append_condition(where.__str__())

if __name__ == "__main__":
    # 示例代码：使用Delete类
    _table_names = ["tableName1", "tableName2"]
    _where = Where("columnName = ?")
    delete_sql = Delete(_table_names, _where)
    print(delete_sql)
