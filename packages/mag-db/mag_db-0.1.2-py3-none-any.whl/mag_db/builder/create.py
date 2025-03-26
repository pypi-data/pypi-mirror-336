from typing import List

from mag_tools.model.symbol import Symbol

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.builder.base_sql import BaseSql
from mag_db.model.engine_type import EngineType
from mag_db.model.operator_type import OperatorType


class Create(BaseSql):
    def __init__(self, table: Table):
        super().__init__('')

        table.check()

        # 添加"Create TABLE 表名1，表名2... ("
        self.append_operator(OperatorType.CREATE_TABLE).append_tables([table]).append_symbol(Symbol.OPEN_PAREN)

        # 添加列名清单
        self.append_whole_columns(table.columns)

        # 添加唯一约束
        self.appendUnique(table.uniques)

        # 添加主键
        self.appendPrimaryKey(table.primary_keys)

        self.append_symbol(Symbol.CLOSE_PAREN)

        self.appendParams(table.comment, table.auto_increment)

        print(f"创建表: {self}")

    def appendPrimaryKey(self, primary_keys: str):
        if primary_keys:
            self.append_operator(OperatorType.PRIMARY_KEY) \
                .append_string_with_symbol(primary_keys, Symbol.OPEN_PAREN)
        else:
            # 移除最后的逗号
            self.remove_last_char().removeLastChar()

    def appendUnique(self, columns: List[Column]):
        for column in columns:
            self.append_operator(OperatorType.UNIQUE) \
                .appendString_with_symbol(",".join(column.uniques), Symbol.OPEN_PAREN) \
                .append_symbol(Symbol.COMMA)

    def appendParams(self, comment: str, auto_increment: int):
        self.append_operator(OperatorType.ENGINE).append_symbol(Symbol.EQUAL).append_string(EngineType.INNO_DB.value)
        if auto_increment > 0:
            self.append_string(OperatorType.AUTO_INCREMENT.name).append_symbol(Symbol.EQUAL).append_long(auto_increment)
        self.append_operator(OperatorType.DEFAULT_CHARSET).append_symbol(Symbol.EQUAL).append_string("utf8") \
            .append_operator(OperatorType.COMMENT).append_symbol(Symbol.EQUAL).append_comment(comment)

if __name__ == '__main__':
    # 示例代码
    _columns = [Column(name="id"), Column(name="name")]
    _table = Table(name="example_table", _columns=_columns, primary_keys="id", comment="示例表", auto_increment=1)
    _create_sql = Create(_table)
    print(_create_sql)
