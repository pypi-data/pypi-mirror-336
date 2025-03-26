
from mag_db.core.db_session import DBSession
from mag_db.sql.update_executor import UpdateExecutor


class IndexAlterExecutor(UpdateExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)
