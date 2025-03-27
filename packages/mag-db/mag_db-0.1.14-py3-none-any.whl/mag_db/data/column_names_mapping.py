from enum import Enum
from inspect import get_annotations
from typing import Dict, List, Optional, Type, TypeVar

from mag_tools.model.base_enum import BaseEnum
from mag_tools.utils.common.class_utils import ClassUtils
from mag_tools.utils.data.string_utils import StringUtils

from mag_db.bean.column import Column

K = TypeVar('K')
V = TypeVar('V')

class ColumnNamesMapping:
    """
    列名信息映射表类
    提供列名信息映射相关的操作。列名格式：“表名.列名” 或 ”列名”，列信息包括列名、类型处理器和映射目标名。
    """
    def __init__(self):
        self.column_infos: Dict[str, str] = {}
        self.column_types: Dict[str, Type] = {}

    def put(self, column_name: str, cls_type: Type, target_name: str):
        """
        放入列名映射
        :param column_name: 列名，可含表名的完整格式，也可不含表名或别名
        :param cls_type: 映射的数据类型
        :param target_name: 映射的目标名
        """
        column_name = StringUtils.pick_head(column_name, " AS ")
        self.column_infos[column_name] = target_name
        self.column_types[column_name] = cls_type

    def get_target_name(self, column_name: str) -> str:
        """
        获取指定列名映射的目标名
        :param column_name: 列名，可含表名和别名的完整格式，也可不含表名或别名
        :return: 映射的目标名
        """
        match_column_name = self.__find_match(list(self.column_infos.keys()), column_name)
        return self.column_infos.get(match_column_name) if match_column_name else None

    def get_class_type(self, column_name: str) -> Type:
        match_column_name = self.__find_match(list(self.column_types.keys()), column_name)
        return self.column_types.get(match_column_name) if match_column_name else None

    @classmethod
    def get_by_class(cls, bean_class: Type, column_names: List[str], column_name_map: Dict[str, str] = None):
        if column_name_map is None:
            column_name_map = {}

        # 缺省地，将Bean的字段名作为数据库列名的映射，然后与设定的映射表合并
        total_map = {column_name: column_name for column_name in column_names}

        # 将旧列名和字段映射表中未包含的列名添加到新表
        for column_name, map_name in column_name_map.items():
            if column_name not in total_map:
                total_map[column_name] = map_name

        return cls.__get_by_bean(total_map, bean_class)

    @classmethod
    def get_by_field_map(cls, field_map: Dict[K, V], column_names: List[str], column_name_map: Optional[Dict[str, str]] = None):
        if column_name_map is None:
            column_name_map = {}

        # 缺省地，将Bean的字段名作为数据库列名的映射，然后与设定的映射表合并
        total_map = {column_name: column_name for column_name in column_names}

        # 将旧列名和字段映射表中未包含的列名添加到新表
        for column_name, map_name in column_name_map.items():
            if column_name not in total_map:
                total_map[column_name] = map_name

        return cls.__get_by_field_map(total_map, field_map)

    @classmethod
    def __get_by_bean(cls, column_names_map: Dict[str, str], bean_class: Type):
        mapping = cls()

        for column_name in column_names_map.keys():
            bean_field_name = Column.to_field_name(column_names_map.get(column_name))
            target_class = get_annotations(bean_class).get(bean_field_name)
            target_class = ClassUtils.get_origin_type(target_class)

            if target_class and issubclass(target_class, Enum):
                target_class = type(target_class.code) if issubclass(target_class, BaseEnum) else target_class.name

            mapping.put(column_name, target_class, bean_field_name)

        return mapping

    @classmethod
    def __get_by_field_map(cls, column_names_map: Dict[str, str], field_map: Dict[K, V]):
        mapping = cls()

        for column_name in column_names_map.keys():
            target_name_type = type(field_map.get(column_name))
            if target_name_type:
                mapping.put(column_name, target_name_type, column_name)

        return mapping

    @classmethod
    def __find_match(cls, column_names: List[str], column_name: str) -> str:
        return next((name for name in column_names if name == column_name or name == StringUtils.pick_tail(column_name, ".")), None)
