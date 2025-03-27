from mag_tools.model.base_enum import BaseEnum

from mag_db.model.sql_type import SqlType


class OracleConvertType(BaseEnum):
    """
    SqlServer的列数据类型-SqlType映射的枚举类

    @description: 建立列类型、对应的类名的映射关系
    @version: v1.2
    @date: 2017/7/22
    """
    # 字符与文本
    CHAR = ("CHAR", SqlType.CHAR, "字符串")
    VARCHAR = ("VARCHAR", SqlType.VARCHAR, "可变字符串")
    VARCHAR2 = ("VARCHAR2", SqlType.VARCHAR, "可变字符串")
    NCHAR = ("NCHAR", SqlType.CHAR, "字符串")
    NVARCHAR = ("NVARCHAR", SqlType.VARCHAR, "可变字符串")
    NVARCHAR2 = ("NVARCHAR2", SqlType.VARCHAR, "可变字符串")
    TEXT = ("TEXT", SqlType.TEXT, "文本")
    # 其它
    BIT = ("BIT", SqlType.BIT, "位")
    BLOB = ("BLOB", SqlType.BLOB, "BLOB")
    RAW = ("RAW", SqlType.BINARY, "二进制")
    BOOLEAN = ("BOOLEAN", SqlType.BOOLEAN, "布尔值")
    ENUM = ("ENUM", SqlType.ENUM, "枚举")
    # 日期和时间
    DATE = ("DATE", SqlType.DATE, "日期")
    TIME = ("TIME", SqlType.TIME, "时间")
    DATETIME = ("DATETIME", SqlType.DATETIME, "日期时间")
    TIMESTAMP = ("TIMESTAMP", SqlType.TIMESTAMP, "时间戳")
    # 数值
    TINYINT = ("TINYINT", SqlType.TINYINT, "小整数")
    LONG = ("LONG", SqlType.BIGINT, "长整数")
    INT = ("INT", SqlType.INT, "整数")
    FLOAT = ("FLOAT", SqlType.FLOAT, "浮点数")
    DOUBLE = ("DOUBLE", SqlType.DOUBLE, "浮点数")
    DECIMAL = ("DECIMAL", SqlType.DECIMAL, "大数")

    def __init__(self, code: str, sql_type: SqlType, desc: str):
        super().__init__(code, desc)
        self.sql_type = sql_type