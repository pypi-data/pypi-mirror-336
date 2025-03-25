
#################################################
# HolAdo (Holistic Automation do)
#
# (C) Copyright 2021-2025 by Eric Klumpp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#################################################

import logging
import abc


logger = logging.getLogger(__name__)



class QueryBuilder():
    """
    Generic Query builder.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, name, db_client=None):
        self.__name = name
        self.__db_client = db_client
    
    @property
    def name(self):
        return self.__name
    
    @property
    def db_client(self):
        return self.__db_client
    
    @db_client.setter
    def db_client(self, client):
        self.__db_client = client
    
    def select(self, table_name, where_data: dict=None, sql_return="*"):
        """
        Simple query & values builder of a select by filtering on given where data.
        Parameter 'where_data' has to be a dictionary with keys equal to table column names.
        """
        raise NotImplementedError

    def insert(self, table_name, data: dict):
        """
        Simple query & values builder of an insert of given data.
        Parameter 'data' has to be a dictionary with keys equal to table column names.
        """
        raise NotImplementedError
    
    def update(self, table_name, data: dict, where_data: dict):
        """
        Simple query & values builder of an update of given data.
        Parameters 'data' and 'where_data' have to be dictionaries with keys equal to table column names.
        """
        raise NotImplementedError
    
    def delete(self, table_name, where_data: dict=None):
        """
        Simple query & values builder of a delete by filtering on given where data.
        Parameter 'where_data' has to be a dictionary with keys equal to table column names.
        """
        raise NotImplementedError
    
    def where(self, query, values, where_data: dict):
        """
        Add where clauses to current couple (query, values), and return a new couple (query, values).
        """
        raise NotImplementedError
    
    def where_in(self, query, values, field_name, field_values, not_in=False):
        """
        Add where in clause to current couple (query, values), and return a new couple (query, values).
        """
        raise NotImplementedError
        
    
    def to_sql(self, query):
        raise NotImplementedError
        