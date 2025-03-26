from mag_tools.model.base_enum import BaseEnum

class DbType(BaseEnum):
    MYSQL = ("mysql", 3306, "MySQL")
    ORACLE = ("oracle", 1521, "Oracle")
    SQL_SERVER = ("sqlserver", 1433, "SQL Server")
    POSTGRE_SQL = ("postgresql", 5432, "PostgreSQL")
    DM = ("dm", 5236, "DM")
    DB2 = ("db2", 5000, "DB2")

    def __init__(self, code:str, port:int, desc:str):
        super().__init__(code, desc)
        self.__port = port

    @property
    def port(self):
        return self.__port

if __name__ == '__main__':
    # 示例用法
    _db_type = DbType.of_code("mysql")
    print(f"Code: {_db_type.code}, Desc: {_db_type.desc}, Port: {_db_type.port}, Display Name: {_db_type.desc}")
