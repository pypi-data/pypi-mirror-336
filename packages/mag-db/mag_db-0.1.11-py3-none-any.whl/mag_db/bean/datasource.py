import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from mag_db.model.db_type import DbType


@dataclass
class Datasource(BaseModel):
    name: Optional[str] = Field(None, alias='数据源名')
    sn: Optional[int] = Field(None, description="数据源序号")
    host: Optional[str] = Field(None, alias="host")
    port: Optional[int] = Field(None, alias="port")
    username: Optional[str] = Field(None, alias="username")
    password: Optional[str] = Field(None, alias="password")
    db_name: Optional[str] = Field(None, alias="db_name")
    db_type: Optional[str] = Field(DbType.MYSQL, alias="db_type")
    driver_class_name: Optional[str] = Field(None, alias="driver-class-name")
    max_wait: Optional[int] = Field(3000, alias="max-wait")
    min_idle: Optional[int] = Field(5, alias="min-idle")
    max_idle: Optional[int] = Field(50, alias="max-idle")
    max_active: Optional[int] = Field(50, alias="max-active")
    test_on_borrow: Optional[bool] = Field(True, alias="test-on-borrow")
    validate_query: Optional[str] = Field("SELECT 1", alias="validate-query")
    initial_size: Optional[int] = Field(None, alias="initial-size")
    time_between_evict: Optional[int] = Field(None, alias="time-between-eviction-runs-millis")
    num_tests_per_evict: Optional[int] = Field(None, alias="num-tests-per-eviction-run")
    min_evict_idle_time: Optional[int] = Field(None, alias="min-evictable-idle-time-millis")
    max_insert: Optional[int] = Field(1000, alias="max-insert")
    fields_terminated: Optional[str] = Field("\\t", alias="fields-terminated")
    enclosed: Optional[str] = Field(None, alias="enclosed")
    lines_terminated: Optional[str] = Field("\\r\\n", alias="lines-terminated")
    ignore_lines: Optional[int] = Field(1, alias="ignore-lines")
    encrypted: Optional[bool] = Field(False, description="是否加密密码")
    crypt_alg: Optional[str] = Field("AES", description="加密算法，缺省为AES")
    encrypt_key: Optional[str] = Field(None, description="加密密钥")
    encoding: Optional[str] = Field("utf-8", description="编码格式")
    default_page_size: Optional[int] = Field(10, description="查询时缺省页面大小")
    log_sql: Optional[bool] = Field(True, description="是否记录SQL语句")
    evict: Optional[bool] = Field(True, description="连接池后台是否清理")
    server_timezone: Optional[str] = Field("GMT+8", description="服务器时区")
    use_ssl: Optional[bool] = Field(False, description="是否使用SSL")
    auto_reconnect: Optional[bool] = Field(True, description="是否自动重连接")
    fail_over_read_only: Optional[bool] = Field(False, description="是否只读失败转移")
    allow_public_key_retrieval: Optional[bool] = Field(True, description="是否允许公钥检索")
    comment: Optional[str] = Field(None, description="备注")
    table_number: Optional[int] = Field(None, description="表数目")

    def __init__(self, **data):
        super().__init__(**data)

    @property
    def can_connect(self) -> bool:
        """
        判定是否可直联
        :return: 是否可直联
        """
        try:
            self.check()
            return self.host is not None and self.username is not None and self.username != "" and self.db_name is not None and self.db_name != ""
        except Exception as e:
            print(f"Error: {e}")
            return False

    def check(self):
        """
        检查数据源信息的有效性
        """
        if not self.url:
            raise ValueError("URL不能为空")
        if not self.username:
            raise ValueError("用户名不能为空")
        if not self.password:
            raise ValueError("密码不能为空")

    @classmethod
    def from_config(cls, config: Dict[str, Any]):
        """
        从配置信息中加载字段
        :param config: 配置信息
        """
        try:
            ds_info = config.get("datasource") if "datasource" in config else config
            return cls(**ds_info)
        except Exception as e:
            print(f"Error loading configuration from dict: {e}")

    @classmethod
    def from_file(cls, cfg_file):
        """
        从文件中读取配置并加载字段
        :param cfg_file: 配置文件路径
        """
        try:
            with open(cfg_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                ds_info = data.get("datasource") if "datasource" in data else data.get("datasource")

            return cls.from_config(ds_info)
        except Exception as e:
            print(f"Error loading configuration from file: {e}")


if __name__ == "__main__":
    _ds = Datasource.from_file('..\\..\\docs\\config\\db_config.json')
    print(_ds)
