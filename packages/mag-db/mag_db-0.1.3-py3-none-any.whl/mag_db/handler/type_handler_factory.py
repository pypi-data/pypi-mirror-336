from typing import Type, Dict
from decimal import Decimal
from datetime import date, time, datetime

from mag_tools.exception.dao_exception import DaoException

from mag_db.handler.bool_type_handler import BoolTypeHandler
from mag_db.handler.bytes_type_handler import BytesTypeHandler
from mag_db.handler.date_type_handler import DateTypeHandler
from mag_db.handler.datetime_type_handler import DatetimeTypeHandler
from mag_db.handler.decimal_type_handler import DecimalTypeHandler
from mag_db.handler.float_type_handler import FloatTypeHandler
from mag_db.handler.int_type_handler import IntTypeHandler
from mag_db.handler.string_type_handler import StringTypeHandler
from mag_db.handler.time_type_handler import TimeTypeHandler
from mag_db.handler.type_handler import TypeHandler


class TypeHandlerFactory:
    __instance = None
    __type_map: Dict[Type, TypeHandler] = {}

    def __init__(self):
        self.__type_map[str] = StringTypeHandler()
        self.__type_map[int] = IntTypeHandler()
        self.__type_map[float] = FloatTypeHandler()
        self.__type_map[bool] = BoolTypeHandler()
        self.__type_map[bytes] = BytesTypeHandler()
        self.__type_map[date] = DateTypeHandler()
        self.__type_map[time] = TimeTypeHandler()
        self.__type_map[datetime] = DatetimeTypeHandler()
        self.__type_map[Decimal] = DecimalTypeHandler()

    @classmethod
    def __get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def get(cls, cls_type: Type) -> TypeHandler:
        if cls_type is None:
            raise DaoException("javaType is null")

        try:
            return cls.__get_instance().__type_map.get(cls_type)
        except KeyError:
            raise DaoException(f"No TypeHandler found for type: {cls_type}")
