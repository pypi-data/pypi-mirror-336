from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, TypeVar

from mag_tools.model.base_enum import BaseEnum
from mag_tools.utils.common.class_utils import ClassUtils
from mag_tools.utils.common.string_utils import StringUtils

from mag_db.data.column_names_mapping import ColumnNamesMapping
from mag_db.handler.type_constant import TypeConstant
from mag_db.handler.type_handler import TypeHandler
from mag_db.utils.column_utils import ColumnUtils
from mag_db.utils.dao_utils import DaoUtils

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

@dataclass()
class RowParameter:
    """
    一条记录的参数及类型的列表
    """
    parameters: List[Any] = field(default_factory=list)
    type_handlers: List[TypeHandler] = field(default_factory=list)

    def append(self, parameter: Any, type_handler: TypeHandler) -> None:
        self.parameters.append(parameter)
        self.type_handlers.append(type_handler)

    # def get_parameter_setter(self):
    #     parameter_setter = ParameterSetter()
    #
    #     for i, parameter in enumerate(self.parameters):
    #         type_handler = self.type_handlers[i]
    #         type_handler.set_parameter(parameter_setter, parameter)
    #     return parameter_setter

    def parameters_str(self):
        return ', '.join(map(str, self.parameters))


@dataclass
class IndexParameters:
    __row_parameters: List[RowParameter] = field(default_factory=list)
    __field_of_where: List[Any] = field(default_factory=list)
    __sum_of_params: int = 0

    def set_string(self, parameter: str) -> None:
        self.__set_parameter(parameter, TypeConstant.STRING)

    def set_bytes(self, parameter: bytes) -> None:
        self.__set_parameter(parameter, TypeConstant.BYTES)

    def set_int(self, parameter: int) -> None:
        self.__set_parameter(parameter, TypeConstant.INT)

    def set_float(self, parameter: float) -> None:
        self.__set_parameter(parameter, TypeConstant.FLOAT)

    def set_decimal(self, parameter: float) -> None:
        self.__set_parameter(parameter, TypeConstant.DECIMAL)

    def set_date(self, parameter: date) -> None:
        self.__set_parameter(parameter, TypeConstant.DATE)

    def set_time(self, parameter: time) -> None:
        self.__set_parameter(parameter, TypeConstant.TIME)

    def set_datetime(self, parameter: datetime) -> None:
        self.__set_parameter(parameter, TypeConstant.DATETIME)

    def set_bool(self, parameter: bool) -> None:
        self.__set_parameter(parameter, TypeConstant.BOOL)

    def set_beans(self, param_beans: List[T], column_names: List[str],
                  column_name_map: Optional[Dict[str, str]] = None) -> None:
        if param_beans:
            column_names_mapping = ColumnNamesMapping.get_by_class(type(param_beans[0]), column_names, column_name_map)
            field_names = ColumnUtils.to_field_names(column_names, column_names_mapping)
            for row_index, param_bean in enumerate(param_beans):
                self.__put_bean(param_bean, field_names, row_index)

    # def set_field_map(self, field_map: Dict[K, V], column_names: List[str]) -> None:
    #     column_names_mapping = ColumnNamesMapping.get_by_field_map(field_map, column_names, column_name_map)
    #     field_names = ColumnUtils.to_field_names(column_names, column_names_mapping)
    #     self.__put_map(field_map, field_names)

    def set_field_maps(self, field_maps: List[Dict[K, V]], column_names: List[str]) -> None:
        if field_maps:
            column_names_mapping = ColumnNamesMapping.get_by_field_map(field_maps[0], column_names)
            field_names = ColumnUtils.to_field_names(column_names, column_names_mapping)
            for row_index, field_map in enumerate(field_maps):
                self.__put_map(field_map, field_names, row_index)

    def set_fields_of_where(self, params: List[T]) -> None:
        self.__field_of_where = []
        for param in params:
            if isinstance(param, Enum):
                self.__field_of_where.append(param.code if isinstance(param, BaseEnum) else param.name)
            else:
                self.__field_of_where.append(param)

    @property
    def row_count(self) -> int:
        return len(self.__row_parameters) if len(self.__row_parameters) > 0 else len(self.__field_of_where)

    @property
    def sum_of_params(self) -> int:
        return self.__sum_of_params

    @property
    def field_num(self):
        return len(self.__field_of_where)

    @property
    def parameters(self)->tuple[tuple[Any,...],...]:
        rows = [tuple(row.parameters) for row in self.__row_parameters]
        return tuple(rows)

    def type_handlers(self, row_index: int = 0)->List[TypeHandler]:
        return self.__row_parameters[row_index].type_handlers if row_index < len(self.__row_parameters) else None

    def get_values(self)-> tuple[tuple[Any, ...], ...]:
        all_values: List[Tuple[Any, ...]] = []

        for row_parameter in self.__row_parameters:
            parameters_of_fow = list(row_parameter.parameters)
            if self.__field_of_where:
                parameters_of_fow.extend(self.__field_of_where)

            all_values.append(tuple(parameters_of_fow))

        if len(self.__row_parameters) == 0 and len(self.__field_of_where) > 0:
            all_values.append(tuple(self.__field_of_where))

        return tuple(all_values)
    #
    # def get_parameters_setters(self) -> List[ParameterSetter]:
    #     parameter_setters = []
    #
    #     for row_parameter in self.__row_parameters:
    #         parameter_setters.append(row_parameter.get_parameter_setter())
    #
    #     return parameter_setters

    def clear(self):
        self.__row_parameters.clear()
        self.__sum_of_params = 0

    def is_empty(self) -> bool:
        return len(self.__row_parameters) == 0 and len(self.__field_of_where) == 0

    def __set_parameter(self, parameter: Any, type_handler: TypeHandler, row_index: int = 0) -> None:
        if row_index < len(self.__row_parameters):
            row_parameter = self.__row_parameters[row_index]
        else:
            row_parameter = RowParameter()
            self.__row_parameters.append(row_parameter)

        row_parameter.append(parameter, type_handler)

        self.__sum_of_params += 1

    def __put_bean(self, param_bean: T, column_names: List[str], row_index: int) -> None:
        for column_name in column_names:
            bean_field_name = StringUtils.hump2underline(column_name)

            try:
                bean_field_value = getattr(param_bean, bean_field_name, None)
                bean_field_type = ClassUtils.get_field_type(param_bean, bean_field_name)

                if isinstance(bean_field_value, Enum):
                    bean_field_value = bean_field_value.code if hasattr(bean_field_value, 'code') else bean_field_value.name

                type_handler = DaoUtils.get_type_handler(bean_field_type)
                self.__set_parameter(bean_field_value, type_handler, row_index)
            except AttributeError:
                pass  # 该列名在bean中不存在，跳过

    def __put_map(self, field_set: Dict[str, V], column_names: List[str],  row_index: int) -> None:
        for column_name in column_names:
            field_value = field_set.get(column_name)
            field_type = type(field_value)
            if field_type is None:
                field_type = str

            type_handler = DaoUtils.get_type_handler(field_type)
            self.__set_parameter(field_value, type_handler, row_index)
