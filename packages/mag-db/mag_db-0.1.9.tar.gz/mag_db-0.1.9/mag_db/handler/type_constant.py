from mag_db.handler.bool_type_handler import BoolTypeHandler
from mag_db.handler.bytes_type_handler import BytesTypeHandler
from mag_db.handler.date_type_handler import DateTypeHandler
from mag_db.handler.datetime_type_handler import DatetimeTypeHandler
from mag_db.handler.decimal_type_handler import DecimalTypeHandler
from mag_db.handler.float_type_handler import FloatTypeHandler
from mag_db.handler.int_type_handler import IntTypeHandler
from mag_db.handler.string_type_handler import StringTypeHandler
from mag_db.handler.time_type_handler import TimeTypeHandler


class TypeConstant:
    # TEXT
    STRING = StringTypeHandler()
    # 时间
    DATETIME = DatetimeTypeHandler()
    DATE = DateTypeHandler()
    TIME = TimeTypeHandler()
    # 数值
    INT = IntTypeHandler()
    FLOAT = FloatTypeHandler()
    DECIMAL = DecimalTypeHandler()
    # 二进制
    BYTES = BytesTypeHandler()
    # 其它
    BOOL = BoolTypeHandler()

