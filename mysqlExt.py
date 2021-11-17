#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from config import global_config
from logger import mylogger

__author__ = 'shgdym'
DB_HOST = global_config.getRaw('mysql', 'DB_HOST')
DB_USER = global_config.getRaw('mysql', 'DB_USER')
DB_PASS = global_config.getRaw('mysql', 'DB_PASS')
DB_NAME = global_config.getRaw('mysql', 'DB_NAME')
DB_PORT = int(global_config.getRaw('mysql', 'DB_PORT'))



class MySql:
    def __init__(self):
        self.cache = []
        self.connect()

    def connect(self):
        if 'cursor' in locals().keys():
            pass
        else:
            self.dbconn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, port=DB_PORT, charset='utf8mb4')
            self.cursor = self.dbconn.cursor()

    def get_rows(self, query_sql):
        """
        return select sql rows
        :param query_sql: select sql
        :return: rows type:set
        """
        self.cursor.execute(query_sql)
        results = self.cursor.fetchall()
        return results

    def get_first_row(self, query_sql):
        """
        return select sql first row
        :param query_sql:
        :return: row  type:set
        """
        res = self.get_rows(query_sql)
        if len(res) == 0:
            return ""
        return res[0]

    def get_first_row_column(self, query_sql):
        """
        return select sql first row Column
        :param query_sql:
        :return: first row column type: str
        """
        row = self.get_first_row(query_sql)
        if row == "":
            return ""
        return row[0]

    def query(self, query_sql):
        """
        run query sql
        :param query_sql: DDL, DML sql
        """
        try:
            self.cursor.execute(query_sql)
            self.dbconn.commit()
        except:
            mylogger.error('ERROR QUERY SQL:'+query_sql)

    def is_table_exists(self, table_name):
        """
        check table exists or not
        :param table_name:
        :return: boole
        """
        if table_name in self.cache:
            return True
        sql = "SHOW TABLES LIKE '" + table_name + "'"
        t = self.get_first_row(sql)
        if t:
            self.cache.append(t[0])
            return True
        return False

    def get_create_table_sql(self, table_name):
        """
        get CreateTable Sql by table name
        :param table_name:
        :return: CreateTable Sql
        """
        sql = "SHOW CREATE TABLE `" + table_name + "`"
        first_row = self.get_first_row(sql)
        return first_row[1]

    def duplicate_table(self, default_tb, new_tb):
        """
        duplicate Table by table name
        :param default_tb: default table name
        :param new_tb: new table name
        """
        create_sql = self.get_create_table_sql(default_tb)
        search_text = "CREATE TABLE `" + default_tb + "`"

        if search_text not in create_sql:
            import sys
            try:
                sys.exit(0)
            except:
                mylogger.error('die')
        new_str = "CREATE TABLE `" + new_tb + "`"
        self.query(create_sql.replace(search_text, new_str, 1))

    def close(self):
        self.cursor.close()

