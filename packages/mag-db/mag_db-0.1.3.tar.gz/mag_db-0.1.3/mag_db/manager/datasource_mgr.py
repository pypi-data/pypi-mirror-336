from typing import Optional

from mag_tools.config.sys_config import SysConfig

from mag_db.core.db_session import DBSession
from mag_db.bean.datasource import Datasource


class DatasourceMgr:
    __instance = None

    @classmethod
    def __get_instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.datasources = {}
        for key, value in SysConfig.get_map('datasources').items():
            ds = Datasource.from_config(value)
            ds.name = key.lower()
            self.datasources[ds.name] = ds

    @classmethod
    def get_datasource(cls, datasource_name: str) -> Optional[Datasource]:
        return cls.__get_instance().datasources.get(datasource_name.lower(), None)

    @classmethod
    def create_session(cls, datasource_name: str) -> Optional[DBSession]:
        ds = cls.get_datasource(datasource_name)
        return DBSession(ds) if ds else None