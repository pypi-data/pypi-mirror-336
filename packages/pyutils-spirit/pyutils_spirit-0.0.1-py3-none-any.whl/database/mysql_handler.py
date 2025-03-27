# @Coding: UTF-8
# @Time: 2024/9/11 0:15
# @Author: xieyang_ls
# @Filename: mysql_handler.py

from abc import ABC, abstractmethod

from logging import info, error, INFO, basicConfig

from pymysql import Connect, OperationalError

from pyutils_spirit.annotation import singleton

from pyutils_spirit.exception import ArgumentException

basicConfig(level=INFO)


class Handler(ABC):

    @abstractmethod
    def select(self, sql: str) -> tuple:
        pass

    @abstractmethod
    def insert(self, sql: str) -> bool:
        pass

    @abstractmethod
    def update(self, sql: str) -> bool:
        pass

    @abstractmethod
    def delete(self, sql: str) -> bool:
        pass

    @abstractmethod
    def manageExecute(self, sql: str) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def getConnection(self) -> [Connect]:
        pass


@singleton(signature="MysqlHandler")
class MySQLHandler(Handler):
    __cursor = None

    __connection = None

    def __init__(self, args: dict[str, str | int]) -> None:
        try:
            connection: Connect = Connect(
                host=args["host"],
                port=args["port"],
                user=args["user"],
                password=args["password"]
            )
            connection.select_db(args["database"])
            info(f"Connected to database {args['database']} successfully!!!")
            info(f"MySQL version: {connection.get_server_info()}")
            cursor = connection.cursor()
            self.__connection = connection
            self.__cursor = cursor
        except (ArgumentException, OperationalError):
            error(f"Connected to database {args['database']} failure")
            raise ArgumentException("please check connected the database arguments")

    def select(self, sql: str) -> tuple:
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def insert(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def update(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def delete(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def manageExecute(self, sql: str) -> bool:
        try:
            self.__cursor.execute(sql)
            self.__connection.commit()
            return True
        except Exception as e:
            self.__connection.rollback()
            raise e

    def getConnection(self) -> [Connect]:
        return self.__connection, self.__cursor

    def disconnect(self) -> None:
        self.__connection.close()
