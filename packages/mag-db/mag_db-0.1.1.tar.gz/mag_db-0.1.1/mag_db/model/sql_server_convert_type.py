
from mag_tools.model.base_enum import BaseEnum
from mag_db.model.sql_type import SqlType


class SqlServerConvertType(BaseEnum):
    """
    SqlServer的列数据类型-SqlType映射的枚举类

    @description: 建立列类型、对应的类名的映射关系
    @version: v1.2
    @date: 2017/7/22
    """
    # 字符与文本
    CHAR = ("CHAR", SqlType.CHAR, "字符串")
    VARCHAR = ("VARCHAR", SqlType.VARCHAR, "可变字符串")
    NVARCHAR = ("NVARCHAR", SqlType.VARCHAR, "可变字符串")
    NCHAR = ("NCHAR", SqlType.CHAR, "字符串")
    TEXT = ("TEXT", SqlType.TEXT, "文本")
    NTEXT = ("NTEXT", SqlType.TEXT, "文本")
    LONGTEXT = ("LONGTEXT", SqlType.TEXT, "长文本")
    MEDIUMTEXT = ("MEDIUMTEXT", SqlType.TEXT, "中长文本")
    # 其它
    BIT = ("BIT", SqlType.BIT, "位")
    BLOB = ("BLOB", SqlType.BLOB, "BLOB")
    BINARY = ("BINARY", SqlType.BINARY, "二进制")
    VARBINARY = ("VARBINARY", SqlType.VARBINARY, "可变二进制")
    BOOLEAN = ("BOOLEAN", SqlType.BOOLEAN, "布尔值")
    IMAGE = ("IMAGE", SqlType.BLOB, "图像")
    # 日期和时间
    DATE = ("DATE", SqlType.DATE, "日期")
    TIME = ("TIME", SqlType.TIME, "时间")
    DATETIME = ("DATETIME", SqlType.DATETIME, "日期时间")
    SMALLDATETIME = ("SMALLDATETIME", SqlType.DATETIME, "日期时间")
    DATETIME2 = ("DATETIME2", SqlType.DATETIME, "日期时间")
    DATETIMEOFFSET = ("DATETIMEOFFSET", SqlType.DATETIME, "日期时间")
    TIMESTAMP = ("TIMESTAMP", SqlType.VARCHAR, "时间戳")
    # 数值
    TINYINT = ("TINYINT", SqlType.TINYINT, "小整数")
    SMALLINT = ("SMALLINT", SqlType.SMALLINT, "短整数")
    BIGINT = ("BIGINT", SqlType.BIGINT, "长整数")
    INT = ("INT", SqlType.INT, "整数")
    REAL = ("REAL", SqlType.REAL, "浮点数")
    FLOAT = ("FLOAT", SqlType.FLOAT, "浮点数")
    DOUBLE = ("DOUBLE", SqlType.DOUBLE, "浮点数")
    DECIMAL = ("DECIMAL", SqlType.DECIMAL, "大数")
    NUMERIC = ("NUMERIC", SqlType.DECIMAL, "大数")
    MONEY = ("MONEY", SqlType.DECIMAL, "对象")

    def __init__(self, code: str, mysql: SqlType, desc: str):
        super().__init__(code, desc)
        self.mysql = mysql