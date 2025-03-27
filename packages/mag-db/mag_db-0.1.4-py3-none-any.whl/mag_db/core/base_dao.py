from typing import Any, Dict, List

import pymysql
from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType

from mag_db.builder.select import Select
from mag_db.core.db_session import DBSession
from mag_db.manager.datasource_mgr import DatasourceMgr
from mag_db.sql.index_query_executor import IndexQueryExecutor
from mag_db.sql.index_delete_executor import IndexDeleteExecutor
from mag_db.sql.index_insert_executor import IndexInsertExecutor
from mag_db.sql.index_update_executor import IndexUpdateExecutor


class BaseDao:
    _session = None

    def __init__(self):
        datasource = DatasourceMgr.get_datasource('default')
        self._session = DBSession(datasource)

    def set_datasource(self, ds_name: str):
        self._session = DBSession(DatasourceMgr.get_datasource(ds_name))

    def insert_by_sql(self, insert_sql:str)->List[int or str]:
        insert = IndexInsertExecutor(insert_sql, self._session)
        return insert.execute()

    def update_by_sql(self, update_sql:str):
        update = IndexUpdateExecutor(update_sql, self._session)
        return update.execute()

    def query_by_sql(self, query_sql:str)->list[Dict[str, Any]]:
        query = IndexQueryExecutor(query_sql, self._session)
        return query.execute_sql()

    def delete_by_sql(self, delete_sql:str):
        delete =IndexDeleteExecutor(delete_sql, self._session)
        return delete.execute()

    def total_count(self, table_name:str) -> int:
        select = Select([table_name], ['*'], None)
        query = IndexQueryExecutor(select.__str__(), self._session)
        return query.get_count(['*'])

    def test(self) -> bool:
        try:
            with self._session.connect() as conn:
                return conn is not None
        except (DaoException, pymysql.MySQLError) as e:
            Logger.error(LogType.DAO, e)
            return False

    @property
    def datasource_name(self):
        return self._session.datasource_name