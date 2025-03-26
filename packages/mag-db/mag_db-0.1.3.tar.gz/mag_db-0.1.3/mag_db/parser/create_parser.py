import re
from typing import List, Optional, Tuple

import sqlparse
from mag_tools.exception.dao_exception import DaoException
from mag_tools.utils.common.string_utils import StringUtils
from sqlparse.sql import Statement
from sqlparse.tokens import Token

from mag_db.bean.column import Column
from mag_db.bean.foreign_key import ForeignKey
from mag_db.bean.primary_key import PrimaryKey
from mag_db.bean.table_info import TableInfo
from mag_db.model.sql_type import SqlType
from mag_db.parser.base_parser import BaseParser


class CreateParser(BaseParser):
    def _parse(self, stmt: Statement) -> TableInfo:
        # 提取表名及别名
        tables = super()._find_table(stmt, {'EXISTS', 'TABLE'})

        charset_token = super()._find_keyword(stmt, 'CHARSET')
        charset = super()._get_value_of_token(stmt, charset_token)

        engine_token = super()._find_keyword(stmt, 'ENGINE')
        engine = super()._get_value_of_token(stmt, engine_token)

        comment_token = super()._find_keyword(stmt, 'COMMENT')
        comment = super()._get_value_of_token(stmt, comment_token)

        auto_increment_token = super()._find_keyword(stmt, 'AUTO_INCREMENT')
        auto_increment = super()._get_value_of_token(stmt, auto_increment_token)

        # 提取列名及其数据类型、约束和注释
        columns_token = super()._find_parenthesis(stmt)
        column_items = self.__split_columns_str(columns_token.value)

        columns = []
        primary_key = None
        foreign_keys = []
        for item in column_items:
            item = item.strip()
            if item.startswith('FOREIGN KEY'):
                foreign_key = self.__parse_foreign_key(item)
                foreign_keys.append(foreign_key)
            elif item.startswith('PRIMARY KEY') or item.startswith('CONSTRAINT'):
                primary_key = self.__parse_primary_key(item)
            else:
                column = self.__parse_column(item)
                columns.append(column)
                if column.is_primary_key:
                    primary_key = PrimaryKey([column.name])

        if primary_key and auto_increment:
            primary_key.increment = auto_increment

        return TableInfo(tables, columns, primary_key=primary_key, foreign_keys=foreign_keys, charset=charset,
                         engine=engine, comment=comment)

    @classmethod
    def __parse_column(cls, column_str: str) -> Column:
        column_stmt = sqlparse.parse(column_str)[0]

        column_name_token = column_stmt.tokens[0]
        if not column_name_token or not isinstance(column_name_token, sqlparse.sql.Identifier):
            raise DaoException(f'找不到列名[{column_str}]')
        column_name = column_name_token.value if column_name_token.value else None

        type_token = super()._next_token(column_stmt, column_name_token)

        if not type_token or type_token.ttype not in (None, Token.Name.Builtin):
            raise DaoException(f'找不到列名[{column_str}]的数据类型')
        sql_type, column_size, decimal = cls.__parse_column_type(type_token.value)

        comment_token = super()._find_keyword(column_stmt, 'COMMENT')
        comment = super()._get_value_of_token(column_stmt, comment_token)

        primary_token = super()._find_keyword(column_stmt, 'PRIMARY KEY')
        is_primary_key = primary_token is not None

        auto_increment_token = super()._find_keyword(column_stmt, 'AUTO_INCREMENT')
        is_auto_increment = auto_increment_token is not None

        return Column(column_name, sql_type=sql_type, column_size=column_size, decimal_digits = decimal, _comment=comment,
                      is_primary_key=is_primary_key, is_auto_increment=is_auto_increment)

    @classmethod
    def __parse_foreign_key(cls, foreign_key_str: str) -> Optional[ForeignKey]:
        if foreign_key_str is None:
            return None

        foreign_key_stmt = sqlparse.parse(foreign_key_str)[0]
        column_names_token = super()._find_keyword(foreign_key_stmt, 'KEY')
        column_names_values = super()._get_value_of_token(foreign_key_stmt, column_names_token)

        if not column_names_values:
            raise DaoException(f'外键语句[{foreign_key_str}]中找不到列名')

        column_names_values = column_names_values.strip('()')
        column_names = [col.strip() for col in column_names_values.split(',')] if column_names_values else None

        references_token = super()._find_keyword(foreign_key_stmt, 'REFERENCES')
        references_value = super()._get_value_of_token(foreign_key_stmt, references_token)
        references_table, references_columns_str, _ = StringUtils.split_by_keyword(references_value, '()')
        references_columns = references_columns_str.split(',') if references_columns_str else None

        return ForeignKey(column_names, references_table, references_columns)

    @classmethod
    def __parse_primary_key(cls, primary_key_str: str) -> Optional[PrimaryKey]:
        if primary_key_str is None:
            return None

        primary_key_stmt = sqlparse.parse(primary_key_str)[0]
        pk_name_token = super()._find_keyword(primary_key_stmt, 'CONSTRAINT')
        pk_name = super()._get_value_of_token(primary_key_stmt, pk_name_token)

        column_names_token = super()._find_keyword(primary_key_stmt, 'PRIMARY KEY')
        column_names_values = super()._get_value_of_token(primary_key_stmt, column_names_token)

        if not column_names_values:
            raise DaoException(f'主键语句[{primary_key_str}]中找不到列名')

        column_names_values = column_names_values.strip('()')
        column_names = [col.strip() for col in column_names_values.split(',')] if column_names_values else None

        key_seq = [index for index, column_name in enumerate(column_names)] if column_names else None

        key_seq_token = super()._find_keyword(primary_key_stmt, 'KEY_SEQ')
        if key_seq_token:
            key_seq_values = super()._get_value_of_token(primary_key_stmt, key_seq_token)
            key_seq_values = key_seq_values.strip('()')
            key_seq = [key.strip() for key in key_seq_values.split(',')] if key_seq_values else None

        return PrimaryKey(column_names, key_seq, pk_name)

    @classmethod
    def __parse_column_type(cls, type_str: str) -> Tuple[Optional[SqlType], Optional[int], Optional[int]]:
        """
        解析SQL列描述字符串，提取数据类型、长度和小数秒精度

        参数:
        description (str): 列描述字符串

        返回:
        包含数据类型、长度和小数秒精度的元组
        """
        pattern = r"(?P<data_type>\w+)(\((?P<length>\d+)(, (?P<decimal>\d+))?\))?"
        match = re.search(pattern, type_str.strip())
        if not match:
            raise ValueError("Invalid column description format")

        column_info = match.groupdict()
        sql_type = SqlType.of_code(column_info.get('data_type'))
        length = column_info.get('length')
        decimal = column_info.get('decimal')
        return sql_type, int(length) if length else None, int(decimal) if decimal else None

    @classmethod
    def __split_columns_str(cls, columns_str: str) -> List[str]:
        pattern = r"('[^']*'|\"[^\"]*\"|\([^)]*\))"

        columns_str = columns_str.strip().replace('\n', '')
        columns_str = columns_str[1:-1] if len(columns_str) > 1 else columns_str
        columns_str = re.sub(pattern, lambda m: m.group().replace(',', '%%'), columns_str)
        return [column_str.replace('%%', ',') for column_str in columns_str.split(",")]

if __name__ == "__main__":
    _sql = '''
    CREATE TABLE IF NOT EXISTS table_name1 (
        id INT  COMMENT '主键ID', 
        name VARCHAR(50) NOT NULL COMMENT '名称',
        length1 DECIMAL(10,2) NULL COMMENT '长度,缺省值为0',
        created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间,缺省为当天", 
        FOREIGN KEY (id,name) REFERENCES other_table(id,name),
        CONSTRAINT pk_name PRIMARY KEY (id, name) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='示例表';
    '''

    _stmt = sqlparse.parse(_sql)[0]
    parser = CreateParser(_stmt)
    if parser.table_info:
        print(parser.table_info)
