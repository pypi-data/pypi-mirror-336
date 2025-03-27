
import pymysql
from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.bean.datasource import Datasource
from mag_db.core.transaction import Transaction
from mag_db.core.transaction_cache import TransactionCache
from mag_db.model.db_type import DbType


class DBSession:
    def __init__(self, datasource: Datasource):
        self._datasource = datasource

    @property
    def datasource_name(self):
        return self._datasource.name

    @property
    def max_insert(self):
        return self._datasource.max_insert

    def connect(self):
        connection = None
        try:
            if self._datasource.db_type == DbType.MYSQL:
                connection = pymysql.connect(
                    host=self._datasource.host,
                    port=self._datasource.port,
                    user=self._datasource.username,
                    password=self._datasource.password,
                    database=self._datasource.db_name
                )
            elif self._datasource.db_type == DbType.POSTGRE_SQL:
                    connection = None
                    # psycopg2.connect(
                    # host=self.__datasource_info.server_addr,
                    # user=self.__datasource_info.username,
                    # password=self.__datasource_info.password,
                    # dbname=self.__datasource_info.db_name
                    # )
            elif self._datasource.db_type == DbType.SQL_SERVER:
                    connection = None
                # pyodbc.connect(
                #     f"DRIVER={{SQL Server}};SERVER={self.__datasource_info.server_addr};"
                #     f"DATABASE={self.__datasource_info.db_name};UID={self.__datasource_info.username};"
                #     f"PWD={self.__datasource_info.password}"
                # )
            else:
                raise f"不支持的数据库类型: {self._datasource.db_type}"
        except Exception as err:
            Logger.error(LogType.DAO, f"数据库连接失败: {err}")

        return connection

    @classmethod
    def close(cls, connection):
        if connection:
            connection.close()
            Logger.debug("数据库连接已关闭")

    # def create_index_insert(self, sql: str):
    #     try:
    #         return IndexInsertExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建插入执行器失败：{sql}")
    #
    # def create_index_delete(self, sql):
    #     try:
    #         return IndexDeleteExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建删除执行器失败：{sql}")
    #
    # def create_index_update(self, sql):
    #     try:
    #         return IndexUpdateExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建更新执行器失败：{sql}")
    #
    # def create_index_query(self, sql):
    #     try:
    #         return IndexQueryExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建查询执行器失败：{sql}")
    #
    # def create_index_create(self, sql):
    #     try:
    #         return IndexCreateExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建建表执行器失败：{sql}")
    #
    # def create_index_drop(self, sql):
    #     try:
    #         return IndexCreateExecutor(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建删表执行器失败：{sql}")
    #
    # def create_index_alter(self, sql):
    #     try:
    #         return IndexAlterExecutor.create_index_alter(sql, self.__datasource)
    #     except DaoException as dao:
    #         Logger.throw(LogType.DAO, f"创建改表执行器失败：{sql}")

    def begin_transaction(self, name: str):
        try:
            last_tx = TransactionCache.get_current_tx(self._datasource.name)
            if last_tx is None:
                connection = self.connect()
                trans = Transaction(name, self.datasource_name, connection)
                trans.begin_with_connection()
                return trans
            else:
                trans = Transaction.from_parent(last_tx, name)
                trans.begin_without_connection()
                return trans
        except DaoException:
            Logger.throw(LogType.DAO, f"开启事务失败：{name}")

    def begin_new_transaction(self, name: str):
        try:
            connection = self.connect()
            trans = Transaction(name, self.datasource_name, connection)
            trans.begin_with_connection()
            return trans
        except DaoException:
            Logger.throw(LogType.DAO, f"开启新事务失败：{name}")

