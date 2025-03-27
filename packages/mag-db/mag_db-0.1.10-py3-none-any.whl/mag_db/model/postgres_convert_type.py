
from mag_tools.model.base_enum import BaseEnum

from mag_db.model.sql_type import SqlType


class PostgresConvertType(BaseEnum):
    """
    SqlServer的列数据类型-SqlType映射的枚举类

    @description: 建立列类型、对应的类名的映射关系
    @version: v1.2
    @date: 2017/7/22
    """
    # 字符与文本
    CHARACTER = ("CHARACTER", SqlType.CHAR, "字符串")
    CHAR = ("CHAR", SqlType.CHAR, "字符串")
    CHARACTER_VARYING = ("CHARACTER VARYING", SqlType.VARCHAR, "可变字符串")
    VARCHAR = ("VARCHAR", SqlType.VARCHAR, "可变字符串")
    TEXT = ("TEXT", SqlType.TEXT, "文本")
    # 其它
    BYTEA = ("BYTEA", SqlType.BINARY, "二进制数")
    BOOLEAN = ("BOOLEAN", SqlType.BOOLEAN, "布尔值")
    BOOL = ("BOOL", SqlType.BOOLEAN, "布尔值")
    ENUM = ("ENUM", SqlType.ENUM, "枚举")
    CIDR = ("CIDR", SqlType.VARCHAR, "IP地址")
    INET = ("INET", SqlType.VARCHAR, "IP地址")
    MACADDR = ("MACADDR", SqlType.VARCHAR, "MAC地址")
    MACADDR8 = ("MACADDR8", SqlType.VARCHAR, "MAC地址")
    JSON = ("JSON", SqlType.JSON, "JSON文本")
    JSONB = ("JSONB", SqlType.JSON, "JSON文本")
    # 日期和时间
    DATE = ("DATE", SqlType.DATE, "日期")
    TIME = ("TIME", SqlType.TIME, "时间")
    TIMESTAMP = ("TIMESTAMP", SqlType.TIMESTAMP, "时间戳")
    INTERVAL = ("INTERVAL", SqlType.BIGINT, "时间间隔")
    # 数值
    SMALLINT = ("SMALLINT", SqlType.SMALLINT, "短整数")
    INTEGER = ("INTEGER", SqlType.MEDIUMINT, "整数")
    INT4 = ("INT4", SqlType.INT, "整数")
    BIGINT = ("BIGINT", SqlType.BIGINT, "长整数")
    DECIMAL = ("DECIMAL", SqlType.DECIMAL, "大数")
    NUMERIC = ("NUMERIC", SqlType.NUMERIC, "大数")
    REAL = ("REAL", SqlType.FLOAT, "浮点数")
    DOUBLE_PRECISION = ("DOUBLE PRECISION", SqlType.DOUBLE, "双精度浮点数")
    SERIAL = ("SERIAL", SqlType.SERIAL, "自增整数")

    def __init__(self, code: str, mysql: SqlType, desc: str):
        super().__init__(code, desc)
        self.mysql = mysql