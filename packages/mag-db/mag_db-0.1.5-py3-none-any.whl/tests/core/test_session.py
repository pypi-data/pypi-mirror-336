import os
import unittest

import pymysql
from mag_tools.config.sys_config import SysConfig

from mag_db.core.db_session import DBSession
from mag_db.manager.datasource_mgr import DatasourceMgr


class TestDBSession(unittest.TestCase):
    def setUp(self):
        SysConfig.set_root_dir(os.path.dirname(os.getcwd()))
        self.session = DatasourceMgr.create_session('Default')

    def test_connect_mysql(self):
        connection = self.session.connect()
        self.assertIsNotNone(connection)
        connection.close()

    def test_close(self):
        connection = self.session.connect()
        DBSession.close(connection)
        with self.assertRaises(pymysql.MySQLError):
            connection.ping(reconnect=False)

    def test_begin_transaction(self):
        trans = self.session.begin_transaction('test_tx')
        self.assertIsNotNone(trans)
        trans.commit()
        trans.close()

    def test_begin_new_transaction(self):
        trans = self.session.begin_new_transaction('test_tx')
        self.assertIsNotNone(trans)
        trans.commit()
        trans.close()

if __name__ == '__main__':
    unittest.main()
