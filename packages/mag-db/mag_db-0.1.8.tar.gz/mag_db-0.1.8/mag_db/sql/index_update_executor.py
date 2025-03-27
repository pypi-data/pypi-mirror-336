from mag_db.core.db_session import DBSession
from mag_db.sql.update_executor import UpdateExecutor


class IndexUpdateExecutor(UpdateExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)