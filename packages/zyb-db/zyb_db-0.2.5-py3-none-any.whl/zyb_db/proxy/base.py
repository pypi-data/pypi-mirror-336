import abc
import re


class AbstractClient(metaclass=abc.ABCMeta):
    """
    数据库客户端抽象类
    """

    @abc.abstractmethod
    def get_database(self):
        """
        获取可操作数据库
        :return: 数据库表操作对象
        """

    @abc.abstractmethod
    def create_db(self, name):
        """
        获取数据库表操作对象
        :param name: 数据库表名称
        :return: 数据库表操作对象
        """

    @abc.abstractmethod
    def get_default_database(self):
        """获取默认数据库操作对象"""

    @abc.abstractmethod
    def close(self):
        """关闭数据库"""


class AbstractDb(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def name(self):
        """数据库名称"""

    @abc.abstractmethod
    def get_table(self, name):
        """
        获取名称为name的表
        :param name: 表名
        :return:
        """

    @abc.abstractmethod
    def collections(self):
        """获取所有集合"""

    def collection(self, name):
        """同get_table"""
        return self.get_table(name)

    def __getitem__(self, name: str):
        """
        获取名称为name的表
        :param name: 表名
        :return:
        """
        return self.get_table(name)

    def __str__(self):
        return "<Database: '%s'>" % self.name

    @staticmethod
    def _is_valid_name(name):
        """
        检验名称合法性
        :param name: 数据库名称
        :return:
        """
        if not isinstance(name, str):
            raise TypeError("名称类型错误，需为字符串类型")
        if len(name) > 64:
            raise ValueError("名称长度需小于等于64")
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        m = re.match(pattern, name)
        if not m:
            raise ValueError("名称不符合数据库规范名称规范")


class AbstractCollection(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self, filter=None):
        """查找多条条数据"""

    @abc.abstractmethod
    def find_one(self, filter=None):
        """查找一条数据"""

    @abc.abstractmethod
    def insert_one(self, document):
        """插入一条数据"""

    @abc.abstractmethod
    def insert_many(self, documents):
        """插入多条数据"""

    @abc.abstractmethod
    def replace_one(self, filter, replacement):
        """替换一条数据"""

    @abc.abstractmethod
    def update_one(self, filter, update):
        """更新一条数据"""

    @abc.abstractmethod
    def update_many(self, filter, update):
        """插入多条数据"""

    @abc.abstractmethod
    def delete_one(self, filter):
        """删除一条数据"""

    @abc.abstractmethod
    def delete_many(self, filter):
        """删除多条数据"""

    @abc.abstractmethod
    def name(self):
        """获取表名"""

    def __str__(self):
        return "<Table: '%s'>" % self.name


class AbsCursor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def limit(self, limit):
        """限定返回数据条数"""

    @abc.abstractmethod
    def next(self):
        """获取下一条数据"""

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __str__(self):
        return "<ZybCursor Object>"






