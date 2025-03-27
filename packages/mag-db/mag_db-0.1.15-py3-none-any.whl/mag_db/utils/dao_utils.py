from enum import Enum
from typing import Optional, Type

from mag_tools.utils.common.class_utils import ClassUtils
from mag_tools.utils.common.enum_utils import EnumUtils

from mag_db.handler.type_handler import TypeHandler
from mag_db.handler.type_handler_factory import TypeHandlerFactory


class DaoUtils:
    @staticmethod
    def get_type_handler(field_type: Type)->Optional[TypeHandler]:
        """
        根据字段类型获取 TypeHandler

        :param field_type: 字段类型
        :return: TypeHandler
        :raises: DaoException
        """
        # 如果为空，表示该字段在 bean 中不存在
        if field_type is None:
            return None

        type_handler = None
        if not issubclass(field_type, Enum):
            type_handler = TypeHandlerFactory.get(field_type)
        else:
            try:
                enum_value_type = str
                if hasattr(field_type, 'code'):
                    enum_value_type = EnumUtils.get_enum_type(field_type, 'code')

                type_handler = TypeHandlerFactory.get(enum_value_type)
            except AttributeError:
                pass

        return type_handler

    @staticmethod
    def get_count_sql(sql: str) -> str:
        return f"SELECT COUNT(*) AS COUNT_ FROM ({sql}) AS COUNTTB_"


