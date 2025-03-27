from mag_db.data.parameter_setter import ParameterSetter
from mag_db.handler.type_handler import T, TypeHandler


class BoolTypeHandler(TypeHandler):
    def set_parameter(self, setter: ParameterSetter, parameter: T):
        setter.set_bool(parameter)