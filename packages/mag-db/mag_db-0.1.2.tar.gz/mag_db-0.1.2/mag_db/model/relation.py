from mag_tools.model.base_enum import BaseEnum


class Relation(BaseEnum):
    """
    关系比较类型的枚举类

    作者: xlcao
    版本: 1.0
    版权所有: Copyright (c) 2016 by Xiaolong Cao. All rights reserved.
    描述: MORE_THAN 大于；LESS_THAN 小于；EQUAL 等于。
    日期: 2019/8/12
    """
    MORE_THAN = (" > ", "大于")
    MORE_THAN_EQUAL = (" >= ", "大于等于")
    LESS_THAN = (" < ", "小于")
    LESS_THAN_EQUAL = (" <= ", "小于等于")
    EQUAL = (" = ", "等于")
    NOT_EQUAL = (" != ", "不等于")
    LIKE = (" LIKE ", "类似")
    NOT_LIKE = (" NOT LIKE ", "不类似")
    IN = (" IN ", "包含")
    NOT_IN = (" NOT IN ", "不包含")


    @classmethod
    def of(cls, code: str):
        code = f" {code.strip()} "
        for item in cls:
            if item.code == code:
                return item
        raise ValueError(f"{code} is not a valid {cls.__name__}")
