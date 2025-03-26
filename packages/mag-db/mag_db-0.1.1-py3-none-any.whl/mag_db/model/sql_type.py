from enum import Enum
from typing import Type, Optional
from datetime import date, time, datetime
from decimal import Decimal

from mag_tools.model.base_enum import BaseEnum


class SqlType(BaseEnum):
    # 数值
    TINYINT = ("TINYINT", int, "小整数")
    SMALLINT = ("SMALLINT", int, "短整数")
    MEDIUMINT = ("MEDIUMINT", int, "中整数")
    INT = ("INT", int, "整数")
    BIGINT = ("BIGINT", int, "长整数")
    TINYINT_UNSIGNED = ("TINYINT UNSIGNED", int, "无符号小整数")
    SMALLINT_UNSIGNED = ("SMALLINT UNSIGNED", int, "无符号短整数")
    MEDIUMINT_UNSIGNED = ("MEDIUMINT UNSIGNED", int, "无符号中整数")
    INT_UNSIGNED = ("INT UNSIGNED", int, "无符号整数")
    BIGINT_UNSIGNED = ("BIGINT UNSIGNED", int, "无符号长整数")
    FLOAT = ("FLOAT", float, "单精度浮点数")
    DOUBLE = ("DOUBLE", float, "双精度浮点数")
    DOUBLE_PRECISION = ("DOUBLE PRECISION", float, "双精度浮点数")
    REAL = ("REAL", float, "浮点数")
    DECIMAL = ("DECIMAL", Decimal, "大数")
    DECIMAL_UNSIGNED = ("DECIMAL UNSIGNED", Decimal, "无符号大数")
    DEC = ("DEC", Decimal, "大数")
    NUMERIC = ("NUMERIC", Decimal, "大数")
    SERIAL = ("SERIAL", int, "自增整数")
    INT4 = ("INT4", int, "整数")
    # 二进制
    BIT = ("BIT", bytes, "位")
    FIXED = ("FIXED", Decimal, "定点数数据")
    BINARY = ("BINARY", bytes, "二进制数据")
    VARBINARY = ("VARBINARY", bytes, "可变二进制数据")
    TINYBLOB = ("TINYBLOB", bytes, "TINY BLOB")
    MEDIUMBLOB = ("MEDIUMBLOB", bytes, "MEDIUM BLOB")
    BLOB = ("BLOB", bytes, "BLOB")
    LONGBLOB = ("LONGBLOB", bytes, "LONG BLOB")
    RAW = ("RAW", bytes, "二进制数据")
    # Char
    CHAR = ("CHAR", str, "字符串")
    VARCHAR = ("VARCHAR", str, "可变字符串")
    NCHAR = ("NCHAR", str, "字符串")
    VARCHAR2 = ("VARCHAR2", str, "可变字符串")
    NVARCHAR = ("NVARCHAR", str, "可变字符串")
    NVARCHAR_2 = ("NVARCHAR2", str, "可变字符串")
    CHARACTER_VARYING = ("CHARACTER VARYING", str, "可变字符串")
    # Text
    TINYTEXT = ("TINYTEXT", str, "短文本")
    TEXT = ("TEXT", str, "文本")
    MEDIUMTEXT = ("MEDIUMTEXT", str, "中长文本")
    LONGTEXT = ("LONGTEXT", str, "长文本")
    JSON = ("JSON", str, "Json文本")
    NTEXT = ("NTEXT", str, "文本")
    JSONB = ("JSONB", str, "Json文本")
    # 日期时间
    DATE = ("DATE", date, "日期")
    TIME = ("TIME", time, "时间")
    TIMESTAMP = ("TIMESTAMP", datetime, "时间戳")
    DATETIME = ("DATETIME", datetime, "日期时间")
    YEAR = ("YEAR", str, "年份")
    DATETIME_2 = ("DATETIME2", datetime, "日期时间")
    SMALLDATETIME = ("SMALLDATETIME", datetime, "日期时间")
    DATETIMEOFFSET = ("DATETIMEOFFSET", datetime, "日期时间")
    # 几何图形
    GEOMETRY = ("GEOMETRY", object, "几何图形")
    POINT = ("POINT", object, "点")
    LINESTRING = ("LINESTRING", object, "线段")
    POLYGON = ("POLYGON", object, "多边形")
    MULTIPOINT = ("MULTIPOINT", object, "多点")
    MULTILINESTRING = ("MULTILINESTRING", object, "多线段")
    MULTIPOLYGON = ("MULTIPOLYGON", object, "多个多边形")
    GEOMETRYCOLLECTION = ("GEOMETRYCOLLECTION", object, "图形集")
    # 其它
    BOOLEAN = ("BOOLEAN", bool, "布尔值")
    BOOL = ("BOOL", bool, "布尔值")
    ENUM = ("ENUM", Enum, "枚举")
    SET = ("SET", str, "集合")
    MONEY = ("MONEY", Decimal, "货币")
    OBJECT = ("OBJECT", object, "对象")
    IMAGE = ("IMAGE", bytes, "图像")
    CIDR = ("CIDR", str, "IP地址")
    INET = ("INET", str, "IP地址")
    MACADDR = ("MACADDR", str, "MAC地址")
    MACADDR8 = ("MACADDR8", str, "MAC地址")

    def __init__(self, code: str, cls: Type, desc: str):
        super().__init__(code, desc)
        self.__cls = cls

    @classmethod
    def of_class(cls, class_type: Type, size: Optional[int] = None) -> 'SqlType':
        """
        根据列的JDK类型获取对应的枚举值
        :param class_type: 列的JDK类型
        :param size: 列长度
        :return: 对应的枚举值
        """
        if class_type == int:
            return cls.INT
        elif class_type == float:
            return cls.FLOAT
        elif class_type == Decimal:
            return cls.DECIMAL
        elif class_type == bool:
            return cls.BOOLEAN
        elif class_type == str:
            if size is None or size < 127:
                return cls.CHAR
            elif size < 8 * 1024:
                return cls.VARCHAR
            elif size < 64 * 1024:
                return cls.TEXT
            elif size < 16 * 1024 * 1024:
                return cls.MEDIUMTEXT
            else:
                return cls.LONGTEXT
        elif class_type == date:
            return cls.DATE
        elif class_type == time:
            return cls.TIME
        elif class_type == datetime:
            return cls.DATETIME
        else:
            for item in cls:
                if item.__cls == class_type:
                    return item
        raise ValueError(f"{class_type} is not a valid class type for {cls.__name__}")

    @classmethod
    def get_class(cls, code: str) -> Type:
        """
        根据列类型名获取对应的JDK类
        :param code: 列类型名
        :return: 对应的JDK类
        """
        return cls.of_code(code).__cls