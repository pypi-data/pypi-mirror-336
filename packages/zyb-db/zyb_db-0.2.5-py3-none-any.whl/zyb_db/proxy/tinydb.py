import os
from typing import Mapping, Iterable, List
import tinydb
from tinydb.table import Table, Document
from tinydb.queries import Query, where

from .errors import DuplicateKeyError
from .base import AbstractClient, AbstractDb, AbstractCollection, AbsCursor


DATABASE_DATA_PATH = os.environ.get('DATABASE_DATA_PATH', os.path.join(os.path.abspath('..'), '.data'))


# 变更tinydb部分行为
class _ZybTable(Table):

    def insert(self, document):
        """
        插入一条文档
        """

        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Mapping')

        if isinstance(document, Document):
            doc_id = document.doc_id

            self._next_id = None
        else:
            doc_id = self._get_next_id()

        def updater(table: dict):
            if doc_id in table:
                raise ValueError(f'Document with ID {str(doc_id)} '
                                 f'already exists')

            doc = dict(document)
            doc.update({"_id": str(doc_id)})
            table[doc_id] = doc

        self._update_table(updater)

        return doc_id

    def insert_multiple(self, documents: Iterable[Mapping]) -> List[int]:
        doc_ids = []

        def updater(table: dict):
            for document in documents:

                if not isinstance(document, Mapping):
                    raise ValueError('Document is not a Mapping')

                if isinstance(document, Document):
                    # Check if document does not override an existing document
                    if document.doc_id in table:
                        raise ValueError(
                            f'Document with ID {str(document.doc_id)} '
                            f'already exists'
                        )

                    doc_id = document.doc_id
                    doc_ids.append(doc_id)
                    # table[doc_id] = dict(document)
                    doc = dict(document)
                    doc.update({"_id": doc_id})
                    table[doc_id] = doc
                    continue

                doc_id = self._get_next_id()
                doc_ids.append(doc_id)
                # table[doc_id] = dict(document)
                doc = dict(document)
                doc.update({"_id": str(doc_id)})
                table[doc_id] = doc

        self._update_table(updater)

        return doc_ids


tinydb.TinyDB.table_class = _ZybTable


class ProxyTinydbClient(AbstractClient):
    """创建tinydb客户端代理"""

    def __init__(self):
        self._default_database_name = "zyb_db"
        self._dbs = {}

    def get_database(self):
        """获取所有数据库"""
        files = os.listdir(DATABASE_DATA_PATH)
        data = []
        for i in files:
            if i.endswith('.json'):
                name, ext = i.split('.', 1)
                data.append(name)
        return data

    def create_db(self, name):
        """创建并获取数据库"""
        self._db_size_check(name)
        if name in self._dbs:
            db = self._dbs[name]
        else:
            db = Database(name)
            self._dbs[name] = db
        return db

    def _db_size_check(self, db_name):
        """
        检查数据库存储大小，超过阈值时删除数据库文件
        :param db_name:
        :return:
        """

    def get_default_database(self):
        return self.get_database(self._default_database_name)

    def close(self):
        for name in self._dbs.keys():
            db = self._dbs.get(name)
            db.close()
            self._dbs.pop(name)


class Database(AbstractDb):

    def __init__(self, name):
        # 判断名称合法性
        self._is_valid_name(name)
        # 拼接数据库路径
        db_name = os.path.join(DATABASE_DATA_PATH, '.'.join([name, 'json']))
        self._db = tinydb.TinyDB(db_name, create_dirs=True)
        self._name = name

    @property
    def name(self):
        """获取数据库名称"""
        return self._name

    def get_table(self, name):
        """获取数据库表操作对象"""
        self._is_valid_name(name)
        collection = self._db.table(name)
        return Collection(collection)

    def collections(self):
        """获取所有集合"""
        return list(self._db.tables())

    def close(self):
        self._db.close()


class Cursor(AbsCursor):
    """数据库数据查询游标"""

    def __init__(self, cursor):
        self._is_exec_query = False
        self._cursor = cursor

    def limit(self, limit):
        if self._is_exec_query:
            raise ValueError("已执行查询的数据不允许再设置limit")
        if not isinstance(limit, int):
            raise TypeError("limit 需为整型对象")
        if limit < 0:
            raise ValueError("limit 需为大于0的整型对象")
        self._cursor = self._cursor[:limit]
        return self

    def next(self):
        self._is_exec_query = True
        if len(self._cursor) == 0:
            raise StopIteration
        res = self._cursor.pop(0)
        if '_id' in res:
            res.update({'_id': ObjectId(res['_id'])})
        return res


class _ReplaceFields(dict):
    """tinydb执行文档替换操作对象"""

    def __call__(self, field):
        _id = field.get('_id')
        field.clear()
        field.update(self)
        field.update({'_id': _id})


class _WriteResult:
    """数据操作结果对象基类"""

    def __init__(self, acknowledged: bool):
        self.__acknowledged = acknowledged

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__acknowledged})"

    @property
    def acknowledged(self) -> bool:
        return self.__acknowledged


class InsertOneResult(_WriteResult):

    __slots__ = ("__inserted_id",)

    def __init__(self, inserted_id, doc_id, acknowledged):
        self.__inserted_id = inserted_id
        self.__doc_id = doc_id
        super().__init__(acknowledged)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.__inserted_id!r}, acknowledged={self.acknowledged})"
        )

    @property
    def inserted_id(self):
        return self.__inserted_id

    @property
    def doc_id(self):
        return self.__doc_id


class InsertManyResult(_WriteResult):

    __slots__ = ("__inserted_ids",)

    def __init__(self, inserted_ids, acknowledged):
        self.__inserted_ids = inserted_ids
        super().__init__(acknowledged)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.__inserted_ids!r}, acknowledged={self.acknowledged})"
        )

    @property
    def inserted_ids(self):
        return self.__inserted_ids


class UpdateResult(_WriteResult):

    __slots__ = ("__raw_result",)

    def __init__(self, raw_result, acknowledged):
        self.__raw_result = raw_result
        super().__init__(acknowledged)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__raw_result!r}, acknowledged={self.acknowledged})"

    @property
    def raw_result(self):
        return self.__raw_result

    @property
    def matched_count(self) -> int:
        return self.__raw_result.get("n", 0)

    @property
    def modified_count(self) -> int:
        return self.__raw_result.get("nModified")

    @property
    def upserted_id(self):
        return self.__raw_result.get("upserted")


class DeleteResult(_WriteResult):
    __slots__ = ("__raw_result",)

    def __init__(self, raw_result, acknowledged):
        self.__raw_result = raw_result
        super().__init__(acknowledged)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__raw_result!r}, acknowledged={self.acknowledged})"

    @property
    def raw_result(self):
        return self.__raw_result

    @property
    def deleted_count(self) -> int:
        return self.__raw_result.get("n", 0)


class ObjectId:
    """文档id对象"""

    def __init__(self, oid):
        self.__id = oid

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return f"ObjectId('{self!s}')"


class Collection(AbstractCollection):

    def __init__(self, collection):
        self._table = collection

    def __transform_filter(self, sql):
        """字典结构转换为tinydb查询条件"""
        if isinstance(sql, dict):
            if not sql:
                sql = None
            else:
                q = where('_id') != '-1'
                for k, v in sql.items():
                    q = q & (where(k) == v)
                sql = q
        return sql

    def find(self, filter=None):
        """
        查询多条数据
        :param filter: 查询条件
        :return:
        """
        filter = self.__transform_filter(filter)
        if filter is None:
            return Cursor(self._table.all())
        return Cursor(self._table.search(filter))

    def find_one(self, filter=None):
        """
        查询一条数据
        :param filter: 查询条件
        :return:
        """
        filter = self.__transform_filter(filter)
        if filter is None:
            filter = where('_id') != '-1'

        res = self._table.get(filter)
        if res:
            res.update({'_id': ObjectId(res['_id'])})
        return res

    def insert_one(self, document):
        """
        插入一条数据
        :param document: 字典结构的文档数据
        :return:
        """
        if not isinstance(document, dict):
            raise ValueError('插入的数据非字典类型')
        _id = document.get("_id")
        if _id is not None:
            q_id = Query()
            res = self._table.get(q_id._id == _id)
            if res is not None:
                raise DuplicateKeyError(f'_id:{_id} already exists in collection:{self.name}')
            doc_id = self._table.insert(document)
        else:
            doc_id = self._table.insert(document)
            _id = ObjectId(doc_id)
        return InsertOneResult(_id, doc_id, True)

    def insert_many(self, documents):
        """
        插入多条数据
        :param documents: 包含多个字典数据元素的列表
        :return:
        """
        if not isinstance(documents, list):
            raise TypeError("数据类型错误，需为文档数据列表")
        results = self._table.insert_multiple(documents)
        return InsertManyResult([ObjectId(i) for i in results], True)

    def replace_one(self, filter, replacement):
        """
        替换一条文档
        :param filter: 查询条件
        :param replacement: 替换内容
        :return:
        """
        filter = self.__transform_filter(filter)
        res = self._table.get(filter)
        raw_result = {'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': True}
        if res:
            replacement = _ReplaceFields(replacement)
            ids = self._table.update(replacement, doc_ids=[res.doc_id])
            raw_result['n'] = len(ids)
            raw_result['nModified'] = len(ids)
        return UpdateResult(raw_result, True)

    def update_one(self, filter, update):
        """
        更新一条数据
        :param filter: 查询条件
        :param update: 更新内容
        :return:
        """
        if '_id' in update:
            raise ValueError("文档标识id不允许更新")
        filter = self.__transform_filter(filter)

        document = self._table.get(filter)
        raw_result = {'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': True}
        if document:
            ids = self._table.update(update, doc_ids=[document.doc_id])
            raw_result['n'] = len(ids)
            raw_result['nModified'] = len(ids)
        return UpdateResult(raw_result, True)

    def update_many(self, filter, update):
        """
        更新多条数据
        :param filter: 查询条件
        :param update: 更新内容
        :return:
        """
        if '_id' in update:
            raise ValueError("文档标识id不允许更新")
        filter = self.__transform_filter(filter)
        documents = self._table.search(filter)
        raw_result = {'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': True}
        if documents:
            ids = self._table.update(update, doc_ids=[doc.doc_id for doc in documents])
            raw_result['n'] = len(ids)
            raw_result['nModified'] = len(ids)
        return UpdateResult(raw_result, True)

    def delete_one(self, filter):
        """
        删除一条数据
        :param filter: 查询条件
        :return:
        """
        filter = self.__transform_filter(filter)
        document = self._table.get(filter)
        raw_result = {'n': 0, 'ok': 1.0}
        if document:
            ids = self._table.remove(doc_ids=[document.doc_id])
            raw_result['n'] = len(ids)
        return DeleteResult(raw_result, True)

    def delete_many(self, filter=None):
        """
        删除多条数据
        :param filter: 查询条件
        :return:
        """
        filter = self.__transform_filter(filter)
        raw_result = {'n': 0, 'ok': 1.0}
        ids = self._table.remove(filter)
        raw_result['n'] = len(ids)
        return DeleteResult(raw_result, True)

    @property
    def name(self):
        """获取表名称"""
        return self._table.name


