from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.core.transaction_cache import TransactionCache
from mag_db.core.db_session import DBSession
from mag_db.sql.base_executor import BaseExecutor


class UpdateExecutor(BaseExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)

    def execute(self)->int:
        self.check()

        tx = None
        try:
            values = self.prepare()

            tx = TransactionCache.get_current_tx(self._session.datasource_name)
            connection = self.get_connection(tx)
            with connection.cursor() as cursor:
                if values:
                    cursor.executemany(self._sql, values)
                else:
                    cursor.execute(self._sql)

                inserted_num = cursor.rowcount

                if tx:
                    tx.commit()
                else:
                    connection.commit()

                return inserted_num
        except (NotImplementedError, Exception):
            if tx:
                tx.rollback()
            Logger.throw(LogType.DAO,f"执行SQL失败: {self._sql}")
        finally:
            if tx:
                tx.end()