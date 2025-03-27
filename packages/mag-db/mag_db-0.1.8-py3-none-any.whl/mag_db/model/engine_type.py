from mag_tools.model.base_enum import BaseEnum


class EngineType(BaseEnum):
    """
    数据库引擎类型枚举类

    @author: Xiaolong Cao
    @version: v1.2
    @description: 数据库引擎类型包括：MyISAM、InnoDB、MEMORY、MRG_MYISAM、ARCHIVE、CSV、BLACKHOLE、FEDERATED、NDB
    @date: 2017/9/21
    """
    INNO_DB = ("InnoDB", "支持事务处理和外键约束")
    MY_ISAM = ("MyISAM", "不支持事务处理和外键约束，适用于只读数据")
    MEMORY = ("MEMORY", "将数据存储在内存中，适用于临时数据")
    MRG_MYISAM = ("MRG_MYISAM", "将多个MyISAM表合并为一个表")
    ARCHIVE = ("ARCHIVE", "用于存储大量的归档数据")
    CSV = ("CSV", "将数据存储为CSV格式文件")
    BLACKHOLE = ("BLACKHOLE", "不存储数据，仅用于复制")
    FEDERATED = ("FEDERATED", "访问远程数据库中的表")
    NDB = ("NDB", "用于MySQL Cluster，支持高可用性和分布式存储")