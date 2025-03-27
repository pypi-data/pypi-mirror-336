
from mag_db.core.db_session import DBSession
from sql.update_executor import UpdateExecutor


class IndexDropExecutor(UpdateExecutor):
    def __init__(self, sql: str, session: DBSession):
        super().__init__(sql, session)