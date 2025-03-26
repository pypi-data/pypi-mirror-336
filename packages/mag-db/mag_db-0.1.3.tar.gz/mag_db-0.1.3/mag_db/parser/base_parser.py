import re
from typing import List, Optional, Set, Tuple

from mag_tools.exception.dao_exception import DaoException
from mag_tools.log.logger import Logger
from mag_tools.model.log_type import LogType
from mag_tools.utils.common.class_utils import ClassUtils
from sqlparse.sql import Function, Identifier, IdentifierList, Parenthesis, Statement, Token, Values, Where
from sqlparse.tokens import Keyword, String

from mag_db.bean.column import Column
from mag_db.bean.table import Table
from mag_db.bean.table_info import TableInfo


class BaseParser:
    def __init__(self, stmt: Statement):
        self.__sql = stmt.value

        try:
            self.__table_info = self._parse(stmt)
        except Exception as e:
            Logger.throw(LogType.DAO, f"SQL解析错误:{stmt.value}\n{e}")

    @property
    def sql(self):
        return self.__sql

    @property
    def table_info(self) -> TableInfo:
        return self.__table_info

    def _parse(self, stmt: Statement) -> TableInfo:
        raise NotImplementedError("_parse() must be implemented by subclasses")

    @classmethod
    def _find_keyword(cls, stmt: Statement, keyword: str) -> Optional[Keyword]:
        for token in stmt.tokens:
            if isinstance(token, Token) and token.ttype in Keyword and token.value.upper() == keyword.upper():
                return token
        return None

    @classmethod
    def _find_any_keyword(cls, stmt: Statement, keywords: Set[str]) -> Optional[Keyword]:
        return next((cls._find_keyword(stmt, keyword) for keyword in keywords if cls._find_keyword(stmt, keyword)),
                    None)

    @classmethod
    def _get_value_of_token(cls, stmt: Statement, token: Token) -> Optional[str]:
        if not token:
            return None

        next_token = cls._next_token(stmt, token)
        while next_token and not ClassUtils.isinstance(next_token, (Identifier, IdentifierList, Parenthesis, Function)) and next_token.ttype != String.Single:
            next_token = cls._next_token(stmt, next_token)
        return next_token.value if next_token else None

    @classmethod
    def _find_values(cls, stmt: Statement) -> Optional[Values]:
        for token in stmt.tokens:
            if isinstance(token, Values):
                return token
        return None

    @classmethod
    def _find_where(cls, stmt: Statement) -> Optional[Where]:
        for token in stmt.tokens:
            if isinstance(token, Where):
                return token
        return None

    @classmethod
    def _find_parenthesis(cls, stmt: Statement):
        for token in stmt.tokens:
            if isinstance(token, Parenthesis):
                return token
            elif isinstance(token, Token) and token.ttype is None:
                for sub_token in token.tokens:
                    if isinstance(sub_token, Parenthesis):
                        return sub_token
        return None

    @classmethod
    def _next_token(cls, stmt: Statement, token: Token) -> Optional[Token]:
        if token is None:
            return None

        next_token_tuple = stmt.token_next(stmt.token_index(token))
        return next_token_tuple[1] if next_token_tuple and len(next_token_tuple) > 1 else None

    @classmethod
    def _find_table(cls, stmt: Statement, keywords: Set[str]) -> List[Table]:
        # 提取表名及别名
        table_name_token = cls._find_any_keyword(stmt, keywords)
        table_full_name = cls._get_value_of_token(stmt, table_name_token)  # 包含列名
        table_name, table_alias = cls._parse_alias(table_full_name)

        if not table_name:
            raise DaoException(f'表名{table_name}不存在')

        return [Table(table_name, alias=table_alias)]

    @classmethod
    def _is_keyword(cls, str_: str) -> bool:
        keywords = ["INSERT", "UPDATE", "DELETE", "SELECT", "NOT", "LIKE", "WHERE", "FROM", "IN", "AS", "BY", "GROUP BY",
                    "ORDER BY", "COUNT", "ALIAS", "HAVING", "LIMIT", "OFFSET"]
        return str_ is not None and str_.upper() in keywords

    @classmethod
    def _parse_alias(cls, sql: str) -> Optional[Tuple[str, Optional[str]]]:
        pattern = r'(\w+)(?:\s+AS\s+(\w+))?'
        match = re.search(pattern, sql, re.IGNORECASE)
        if match:
            name = match.group(1)
            alias = match.group(2) if match.group(2) else None
            return name, alias
        return None

    @classmethod
    def _parse_column_names(cls, column_names_str: str) -> List[Column]:
        columns = []
        items = column_names_str.split(',')
        for item in items:
            name, alias = cls._parse_alias(item)
            columns.append(Column(name, alias=alias))
        return columns


