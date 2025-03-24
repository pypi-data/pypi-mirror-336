import os
import json
import pymongo
from bson import ObjectId
from . import QueryInstance
from .base import AbstractClient, AbstractDb, AbstractCollection, AbsCursor


class ProxyMongoClient(AbstractClient):

    def __init__(self):
        # 默认数据库
        uri, self.__default_db_name = self._load_user_info()
        self.client = pymongo.MongoClient(uri)

    def create_db(self, name):
        db = self.client.get_database(self.__default_db_name)
        return Database(db, name)

    def get_database(self):
        databases = self.client.list_databases()
        data = []
        for db in databases:
            data.append(db['name'])
        return data

    def get_default_database(self):
        return Database(self.client.get_default_database(), 'zyb_db')

    def close(self):
        self.client.close()

    # 全局获取
    def _load_user_info(self):
        """
        通过配置文件获取配置信息
        :return:
        """
        filename = os.environ.get("MONGO_CONFIG_FILE", "config.json")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
            uri = data.get("uri", "mongodb://127.0.0.1:27017")
            database = data.get("database", "test")
        else:
            uri = "mongodb://127.0.0.1:27017"
            database = "test"

        return uri, database


class Database(AbstractDb):

    def __init__(self, db, prefix=''):
        self._db = db
        self._is_valid_name(prefix)
        self.__prefix = prefix

    @property
    def name(self):
        return self.__prefix

    def get_table(self, name):
        self._is_valid_name(name)
        _name = '-'.join([self.__prefix, name])
        collection = self._db.get_collection(_name)
        return Collection(collection)

    def collections(self):
        """获取所有集合"""
        return list(self._db.list_collection_names())


class Cursor(AbsCursor):

    def __init__(self, cursor):
        self.cursor = cursor

    def limit(self, limit):
        self.cursor.limit(limit)
        return self

    def next(self):
        return self.cursor.next()


class Collection(AbstractCollection):

    def __init__(self, collection):
        self._table = collection

    def find(self, filter=None):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        cursor = self._table.find(filter)
        return Cursor(cursor)

    def find_one(self, filter=None):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        return self._table.find_one(filter)

    def insert_one(self, document):
        return self._table.insert_one(document)

    def insert_many(self, documents):
        result = self._table.insert_many(documents)
        return result

    def replace_one(self, filter, replacement):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        return self._table.replace_one(filter, replacement)

    def update_one(self, filter, update):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        update = {"$set": update}
        return self._table.update_one(filter, update)

    def update_many(self, filter, update):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        update = {"$set": update}
        return self._table.update_many(filter, update)

    def delete_one(self, filter):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        return self._table.delete_one(filter)

    def delete_many(self, filter):
        if not isinstance(filter, dict):
            filter = self._parse_filter(filter)
        return self._table.delete_many(filter)

    @property
    def name(self):
        return self._table.name

    def _parse_filter(self, filter):
        if filter is not None:
            if not hasattr(filter, '_hash') or not isinstance(filter, QueryInstance):
                raise ValueError("查询条件语法错误")
            filter = self._parse_cond(filter._hash)
        return filter

    def _parse_cond(self, conds, container=None):
        """
        将where条件查询语法转换为mongo查询语法
        :param conds:where查询条件
        :param container: mongo查询条件
        :return:
        """
        if container is None:
            container = {}
        if len(conds) == 2:
            if conds[0] == 'or':
                container["$or"] = []
                for i in list(conds[1]):
                    container["$or"].append(self._parse_cond(i))

            elif conds[0] == 'and':
                container["$and"] = []
                for i in list(conds[1]):
                    container["$and"].append(self._parse_cond(i))
        elif len(conds) == 3:
            operator = conds[0]
            key = conds[1][0]
            value = conds[2]
            if key == '_id' and isinstance(value, str):
                value = ObjectId(value)
            if operator == '==':
                container[key] = value
            elif operator == '!=':
                container[key] = {"$ne": value}
            elif operator == '>':
                container[key] = {"$gt": value}
            elif operator == '>=':
                container[key] = {"$gte": value}
            elif operator == '<':
                container[key] = {"$lt": value}
            elif operator == '<=':
                container[key] = {"$lte": value}

        return container









