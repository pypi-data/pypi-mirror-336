from mag_tools.model.base_enum import BaseEnum


class SynchronMode(BaseEnum):
    """
    数据同步方式的枚举类
    大数据平台的同步方式有几种：
    全量同步：每天新增一个日期分区，同步并存储当天的全量数据，适用于小数据情况；
    全量覆盖：不设置分区，每天直接覆盖原数据；
    实时增量同步：不设置分区，定时上传新增数据。
    """
    FULL_COVER = ("full_coverage", "全量覆盖")
    REAL_INCREASE = ("realtime_increase", "实时增量同步")
    FULL_SYNC = ("full_synchron", "全量同步")
