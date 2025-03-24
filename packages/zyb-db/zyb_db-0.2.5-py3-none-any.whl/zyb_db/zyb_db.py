import os
import threading


class ZybClient:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(ZybClient, cls).__new__(cls, *args, **kwargs)
                db_type = os.environ.get("ZYB_RUN_FLAG")
                if db_type == '1':
                    from .proxy.mongo import ProxyMongoClient
                    cls._instance._client = ProxyMongoClient()
                else:
                    from .proxy.tinydb import ProxyTinydbClient
                    cls._instance._client = ProxyTinydbClient()
        return cls._instance

    def __init__(self, uri="zyb://_default"):
        if not isinstance(uri, str):
            raise TypeError("数据库连接描述符需为字符串")
        if not uri.startswith("zyb://"):
            raise ValueError("数据库连接协议为zyb://开头")

    def __getitem__(self, name: str):
        """获取名称为name的表"""
        return self.create_db(name)

    def create_db(self, name):
        """获取数据库表操作对象"""
        return self._client.create_db(name)

    def get_database(self):
        """获取本地所有数据库"""
        return self._client.get_database()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._client.close()

    def close(self):
        self._client.close()


def db(name):
    client = ZybClient()
    return client.create_db(name)


def all_db():
    client = ZybClient()
    return client.get_database()



