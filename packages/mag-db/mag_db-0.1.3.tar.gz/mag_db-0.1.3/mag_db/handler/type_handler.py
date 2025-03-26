from typing import  TypeVar


from mag_db.data.parameter_setter import ParameterSetter

T = TypeVar('T')

class TypeHandler:
    def set_parameter(self, setter: ParameterSetter, parameter: T):
        raise NotImplementedError("init() must be implemented by subclasses")