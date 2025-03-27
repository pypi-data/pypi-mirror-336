from typing import Dict

from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType


class TransactionGroup:
    def __init__(self):
        self.__tx_group = []

    @property
    def current(self):
        if not self.__tx_group:
            return None
        tx = self.__tx_group[-1]
        if tx is None:
            Logger.throw(LogType.DAO, "Cached transaction is null")
        return tx

    def remove(self, tx):
        self.__tx_group.remove(tx)

    def append(self, tx):
        self.__tx_group.append(tx)

class TransactionCache:
    """
    数据库事务缓存管理类
    """
    __transaction_cache : Dict[str, TransactionGroup] = {}

    @classmethod
    def append_tx(cls, ds_name: str, tx):
        cache = cls.__transaction_cache.get(ds_name, None)
        if cache:
            cache.append(tx)

    @classmethod
    def remove_tx(cls, ds_name: str, tx):
        cache = cls.__transaction_cache.get(ds_name, None)
        if cache:
            cache.remove(tx)

    @classmethod
    def get_cache_by_name(cls, ds_name: str) -> TransactionGroup:
        if ds_name not in cls.__transaction_cache:
            cls.__transaction_cache[ds_name] = TransactionGroup()
        return cls.__transaction_cache[ds_name]

    @classmethod
    def get_current_tx(cls, ds_name: str):
        cache = cls.get_cache_by_name(ds_name)
        return cache.current

    @classmethod
    def close(cls):
        cls.__transaction_cache.clear()

