
from mag_db.builder.base_sql import BaseSql
from mag_db.bean.table import Table
from mag_db.model.operator_type import OperatorType
from mag_tools.model.symbol import Symbol

class LoadData(BaseSql):

    def __init__(self, table_name: str, file: str, local: bool, field_terminated: str, enclosed: str, lines_terminated: str, ignore_lines: int):
        """
        构造LOAD DATA语句（只限于MySql）

        :param table_name: 表名
        :param file: 数据文件路径
        :param local: 文件是否从客户端本地加载
        :param field_terminated: 字段分隔符
        :param enclosed: 包含符
        :param lines_terminated: 行分隔符
        :param ignore_lines: 忽略的行数
        """
        super().__init__()

        self.append_operator(OperatorType.LOAD_DATA)
        if local:
            self.append_operator(OperatorType.LOCAL)
        self.append_operator(OperatorType.INFILE)
        self.append_string_with_symbol(file, Symbol.SINGLE_QUOTATION)

        self.append_operator(OperatorType.INTO_TABLE)
        self.append_tables([Table(table_name)])

        self.append_operator(OperatorType.FIELDS_TERMINATED).append_string_with_symbol(field_terminated, Symbol.SINGLE_QUOTATION)
        if enclosed:
            self.append_operator(OperatorType.ENCLOSED).append_string_with_symbol(enclosed, Symbol.SINGLE_QUOTATION)
        self.append_operator(OperatorType.LINES_TERMINATED).append_string_with_symbol(lines_terminated, Symbol.SINGLE_QUOTATION)
        self.append_operator(OperatorType.IGNORE).append_long(ignore_lines).append_operator(OperatorType.LINES)