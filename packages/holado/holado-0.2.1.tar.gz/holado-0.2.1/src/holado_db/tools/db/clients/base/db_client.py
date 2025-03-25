
#################################################
# HolAdo (Holistic Automation do)
#
# (C) Copyright 2023 by Eric Klumpp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#################################################

import logging
from builtins import NotImplementedError
from holado_core.common.exceptions.functional_exception import FunctionalException
from holado_core.common.exceptions.technical_exception import TechnicalException
from holado_core.common.tables.table_with_header import TableWithHeader
from holado_core.common.tables.table_row import TableRow
import abc
from holado_core.common.tools.tools import Tools
from holado_core.common.tables.table import Table
from holado_db.tools.db.query.base.query_builder import QueryBuilder

logger = logging.getLogger(__name__)


class DBClient(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, connect_kwargs, with_cursor=True, auto_commit=True):
        self.__name = name
        self.__connect_kwargs = connect_kwargs
        self.__with_cursor = with_cursor
        self.__auto_commit = auto_commit
        
        self.__connection = None
        self.__query_builder = None
    
    @property
    def name(self):
        return self.__name
    
    @property
    def query_builder(self) -> QueryBuilder:
        return self.__query_builder
    
    @query_builder.setter
    def query_builder(self, builder):
        self.__query_builder = builder
    
    @property
    def is_connected(self):
        return self.__connection is not None
    
    @property
    def connection(self):
        return self.__connection
    
    @property
    def cursor(self):
        if not self.__with_cursor:
            raise TechnicalException(f"DB client '{self.__name}' doesn't manage cursor")
        return self.__cursor
    
    def connect(self):
        try:
            self.__connection = self._connect(**self.__connect_kwargs)
        except Exception as exc:
            Tools.raise_same_exception_type(exc, f"[{self.name}] Failed to connect with parameters {self.__connect_kwargs}")
        if self.__with_cursor:
            self.__cursor = self.__connection.cursor()
    
    def _connect(self, **kwargs):
        raise NotImplementedError()
    
    def _verify_is_connected(self):
        if not self.is_connected:
            raise FunctionalException(f"DB Client '{self.name}' is not connected")
        
    def execute_query(self, query, *args, **kwargs):
        sql = self.query_builder.to_sql(query)
        return self.execute(sql, *args, **kwargs)
        
    def execute(self, sql, *args, **kwargs):
        # Manage commit & auto commit
        do_commit = None
        if 'do_commit' in kwargs:
            do_commit = kwargs.pop('do_commit')
        if do_commit is None:
            do_commit = self.__auto_commit
            
        self._verify_is_connected()
        
        if Tools.do_log(logger, logging.DEBUG):
            logger.debug(f"[{self.name}] Executing SQL [{sql}] with parameters [{args if args else ''}{kwargs if kwargs else ''}]...")
        try:
            if args:
                self.cursor.execute(sql, args)
            elif kwargs:
                self.cursor.execute(sql, kwargs)
            else:
                self.cursor.execute(sql)
        except self._get_base_exception_type() as exc:
            self.rollback()
            raise TechnicalException(f"[{self.name}] Error while executing SQL [{sql}] (args: {args} ; kwargs: {kwargs})") from exc
        
        if self.cursor.description:
            field_names = [field[0] for field in self.cursor.description]
            
            res = TableWithHeader()
            res.header = TableRow(cells_content=field_names)
            
            row_values = self.cursor.fetchone()
            while row_values:
                res.add_row(cells_content=row_values)
                row_values = self.cursor.fetchone()
        elif self.cursor.rowcount > 0:
            res = self.cursor.rowcount
        else:
            res = None
        
        if Tools.do_log(logger, logging.DEBUG):
            logger.debug(f"[{self.name}] Executed SQL [{sql}] with parameters [{args if args else ''}{kwargs if kwargs else ''}] => [{res}]")
        self.__log_sql_result(res)
        
        # Manage commit
        if do_commit:
            try:
                self.commit()
            except self._get_base_exception_type() as exc:
                self.rollback()
                raise TechnicalException(f"[{self.name}] Error while commit after SQL [{sql}] (args: {args} ; kwargs: {kwargs})") from exc
            
        return res
    
    def _get_base_exception_type(self):
        raise NotImplementedError()
    
    def __log_sql_result(self, sql_result, limit_rows=10):
        if Tools.do_log(logger, logging.DEBUG):
            res_str = self.__represent_sql_result(sql_result, limit_rows=limit_rows)
            if '\n' in res_str:
                logger.debug(f"[{self.name}] SQL result:\n{Tools.indent_string(4, res_str)}")
            else:
                logger.debug(f"[{self.name}] SQL result: {res_str}")
    
    def __represent_sql_result(self, sql_result, limit_rows = 10):
        if isinstance(sql_result, Table):
            return sql_result.represent(limit_rows=limit_rows)
        else:
            return str(sql_result)
    
    def commit(self):
        self.connection.commit()
        
    def rollback(self):
        self.connection.rollback()
        
    def exist_table(self, table_name):
        raise NotImplementedError()
    
    def insert(self, table_name, data: dict, do_commit=None):
        """
        Insert given data.
        Parameter 'data' has to be a dictionary with keys equal to table column names.
        """
        query, values = self.query_builder.insert(table_name, data)
        return self.execute_query(query, *values, do_commit=do_commit)
    
    def update(self, table_name, data: dict, where_data: dict, do_commit=None):
        """
        Update given data.
        Parameters 'data' and 'where_data' have to be dictionaries with keys equal to table column names.
        """
        query, values = self.query_builder.update(table_name, data, where_data)
        return self.execute_query(query, *values, do_commit=do_commit)
    
    def select(self, table_name, where_data: dict=None, sql_return="*"):
        """
        Select by filtering on given where data.
        Parameter 'where_data' has to be a dictionary with keys equal to table column names.
        """
        query, values = self.query_builder.select(table_name, where_data, sql_return)
        return self.execute_query(query, *values, do_commit=False)
    
    def delete(self, table_name, where_data: dict=None, do_commit=None):
        """
        Delete by filtering on given where data.
        Parameter 'where_data' has to be a dictionary with keys equal to table column names.
        """
        query, values = self.query_builder.delete(table_name, where_data)
        return self.execute_query(query, *values, do_commit=do_commit)
    
    def set_or_update_json_key_value(self, table_name, field_name, json_key, json_value, where_data):
        """
        Set or update a json field with key=value.
        """
        raise NotImplementedError()
        
    def _get_sql_placeholder(self):
        """
        Return the character/string to use as placeholder in SQL requests.
        """
        raise NotImplementedError()

