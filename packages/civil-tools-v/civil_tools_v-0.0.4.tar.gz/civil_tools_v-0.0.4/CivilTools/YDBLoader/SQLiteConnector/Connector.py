from typing import List
import sqlite3
import os


class Connector:

    def __init__(self, file_path=None):
        self.set_db_file(file_path)
        self.connection = None
        self.cursor = None

    def set_db_file(self, file_path):
        if file_path != None and not os.path.exists(file_path):
            raise AttributeError(
                "The file_path is not existed, please check your file path. "
            )
        self.__file_path = file_path

    def connect(self):
        """
        建立与 SQLite 数据库的连接
        """
        if self.__file_path == None:
            raise AttributeError(
                "The file_path is None, you should set db file path before connect. Try the method [set_db_file]. "
            )
        try:
            self.connection = sqlite3.connect(self.__file_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"连接数据库时出错: {e}")

    def extract_table(self, table_name):
        """
        从指定的表中提取数据
        :param table_name: 要提取数据的表名
        :return: 表中的数据列表
        """
        if self.cursor is None:
            self.connect()
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"从表 {table_name} 提取数据时出错: {e}")
            return []

    def extract_table_by_columns(self, table_name, column_list: List[str]):
        """
        从指定的表中提取数据
        :param table_name: 要提取数据的表名
        :param column_list: 要提取的列名集合
        :return: 表中的数据列表
        """
        if self.cursor is None:
            self.connect()
        try:
            column_list_sql = ",".join(column_list)
            self.cursor.execute(f"SELECT {column_list_sql} FROM {table_name}")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"从表 {table_name} 提取数据时出错: {e}")
            return []

    def extract_table_by_columns_and_filter(
        self, table_name, column_list: List[str], limit_column: str, target_value
    ):
        if self.cursor is None:
            self.connect()
        try:
            column_list_sql = ",".join(column_list)
            self.cursor.execute(
                f"SELECT {column_list_sql} FROM {table_name} WHERE {limit_column}=={target_value}"
            )
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"从表 {table_name} 提取数据时出错: {e}")
            return []

    def is_table_in_db(self, table_name: str):

        if self.cursor is None:
            self.connect()
        try:
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"从表 {table_name} 提取数据时出错: {e}")
            return []

    def close(self):
        """
        关闭数据库连接
        """
        if self.connection:
            self.connection.close()
