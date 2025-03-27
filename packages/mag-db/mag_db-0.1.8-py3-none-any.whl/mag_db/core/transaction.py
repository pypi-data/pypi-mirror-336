from typing import Optional

from pymysql.connections import Connection

from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.core.transaction_cache import TransactionCache


class Transaction:
    def __init__(self, name: str, datasource_name:str, connection: Optional[Connection]=None):
        self.is_commit = False
        self.is_rollback = False
        self.is_end = False
        self.name = name
        self.__datasource_name = datasource_name
        self.__connection = connection
        self.parent = None

    @classmethod
    def from_parent(cls, parent, name: str):
        if parent is None:
            raise DaoException("parent transaction is null")

        parent.assert_open()
        return cls(name, parent.datasource_name, parent.get_connection())

    @property
    def datasource_name(self):
        return self.parent.datasource_name if self.parent else self.__datasource_name

    @property
    def connection(self)->Connection:
        return self.parent.connection() if self.parent else self.__connection

    def begin_with_connection(self):
        try:
            if self.connection is None:
                raise DaoException("connection is null")

            self.connection.autocommit(False)
            TransactionCache.append_tx(self.datasource_name, self)
        except Exception as e:
            self.close()
            Logger.throw(LogType.DAO, f"启动事务[{self.name}]失败: {str(e)}")

    def begin_without_connection(self):
        TransactionCache.append_tx(self.datasource_name, self)

    def commit(self):
        if self.is_commit or self.is_end:
            Logger.throw(LogType.DAO, f"提交事务[{self.name}]失败")

        try:
            self.do_commit()
        finally:
            self.is_commit = True

    def rollback(self):
        if self.is_rollback or self.is_end:
            Logger.throw(LogType.DAO, f"回滚事务[{self.name}]失败")

        try:
            self.do_rollback()
        finally:
            self.is_rollback = True

    def end(self):
        if self.is_end:
            Logger.throw(LogType.DAO, f"结束事务[{self.name}]失败")

        try:
            self.do_end()
            if not self.is_commit and not self.is_rollback:
                Logger.throw(LogType.DAO, f"结束事务[{self.name}]失败")
        finally:
            self.is_end = True

    def assert_open(self):
        if self.is_end or self.is_commit or self.is_rollback:
            Logger.throw(LogType.DAO,  f"事务[{self.name}]未打开")

    def do_rollback(self):
        try:
            if self.parent is None and self.connection:
                self.connection.rollback()
                self.connection.autocommit(True)
        except Exception as e:
            Logger.throw(LogType.DAO, f"回滚事务[{self.name}]失败：{str(e)}")

    def do_end(self):
        try:
            if self.parent is None:
                self.close()
        finally:
            TransactionCache.remove_tx(self.datasource_name, self)

    def close(self):
        try:
            if self.__connection:
                self.__connection.close()
        except Exception as e:
            Logger.throw(LogType.DAO, f"关闭事务[{self.name}]失败：{str(e)}")
        finally:
            self.__connection = None

    def do_commit(self):
        try:
            if self.parent is None:
                self.__connection.commit()
                self.__connection.autocommit(True)
        except Exception as e:
            Logger.throw(LogType.DAO, f"提交事务[{self.name}]失败：{str(e)}")