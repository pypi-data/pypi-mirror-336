# copy from tinydb and reference to tinydb.queries

import re
import sys
from typing import Mapping, Tuple, Callable, Any, Union, List, Optional


__all__ = ('get',)


class FrozenDict(dict):

    def __hash__(self):
        # Calculate the has by hashing a tuple of all dict items
        return hash(tuple(sorted(self.items())))

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    # Disable write access to the dict
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    setdefault = _immutable  # type: ignore
    popitem = _immutable

    def update(self, e=None, **f):
        raise TypeError('object is immutable')

    def pop(self, k, d=None):
        raise TypeError('object is immutable')


def freeze(obj):
    """
    Freeze an object by making it immutable and thus hashable.
    """
    if isinstance(obj, dict):
        # Transform dicts into ``FrozenDict``s
        return FrozenDict((k, freeze(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        # Transform lists into tuples
        return tuple(freeze(el) for el in obj)
    elif isinstance(obj, set):
        # Transform sets into ``frozenset``s
        return frozenset(obj)
    else:
        # Don't handle all other objects
        return obj


def is_sequence(obj):
    return hasattr(obj, '__iter__')


class QueryInstance:

    def __init__(self, test: Callable[[Mapping], bool], hashval: Optional[Tuple]):
        self._test = test
        self._hash = hashval

    def is_cacheable(self) -> bool:
        return self._hash is not None

    def __call__(self, value: Mapping) -> bool:
        return self._test(value)

    def __hash__(self) -> int:
        return hash(self._hash)

    def __repr__(self):
        return 'QueryImpl{}'.format(self._hash)

    def __eq__(self, other: object):
        if isinstance(other, QueryInstance):
            return self._hash == other._hash

        return False

    def __and__(self, other: 'QueryInstance') -> 'QueryInstance':
        if self.is_cacheable() and other.is_cacheable():
            hashval = ('and', frozenset([self._hash, other._hash]))
        else:
            hashval = None
        return QueryInstance(lambda value: self(value) and other(value), hashval)

    def __or__(self, other: 'QueryInstance') -> 'QueryInstance':
        if self.is_cacheable() and other.is_cacheable():
            hashval = ('or', frozenset([self._hash, other._hash]))
        else:
            hashval = None
        return QueryInstance(lambda value: self(value) or other(value), hashval)

    def __invert__(self) -> 'QueryInstance':
        hashval = ('not', self._hash) if self.is_cacheable() else None
        return QueryInstance(lambda value: not self(value), hashval)


class Query(QueryInstance):

    def __init__(self) -> None:
        self._path: Tuple[Union[str, Callable], ...] = ()

        def notest(_):
            raise RuntimeError('Empty query was evaluated')

        super().__init__(
            test=notest,
            hashval=(None,)
        )

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    def __hash__(self):
        return super().__hash__()

    def __getattr__(self, item: str):
        query = type(self)()

        query._path = self._path + (item,)

        query._hash = ('path', query._path) if self.is_cacheable() else None

        return query

    def __getitem__(self, item: str):
        return self.__getattr__(item)

    def _generate_test(
            self,
            test: Callable[[Any], bool],
            hashval: Tuple,
            allow_empty_path: bool = False
    ) -> QueryInstance:
        if not self._path and not allow_empty_path:
            raise ValueError('Query has no path')

        def runner(value):
            try:
                # Resolve the path
                for part in self._path:
                    if isinstance(part, str):
                        value = value[part]
                    else:
                        value = part(value)
            except (KeyError, TypeError):
                return False
            else:
                # Perform the specified test
                return test(value)

        return QueryInstance(
            lambda value: runner(value),
            (hashval if self.is_cacheable() else None)
        )

    def __eq__(self, rhs: Any):
        return self._generate_test(
            lambda value: value == rhs,
            ('==', self._path, freeze(rhs))
        )

    def __ne__(self, rhs: Any):
        return self._generate_test(
            lambda value: value != rhs,
            ('!=', self._path, freeze(rhs))
        )

    def __lt__(self, rhs: Any) -> QueryInstance:
        return self._generate_test(
            lambda value: value < rhs,
            ('<', self._path, rhs)
        )

    def __le__(self, rhs: Any) -> QueryInstance:
        return self._generate_test(
            lambda value: value <= rhs,
            ('<=', self._path, rhs)
        )

    def __gt__(self, rhs: Any) -> QueryInstance:
        return self._generate_test(
            lambda value: value > rhs,
            ('>', self._path, rhs)
        )

    def __ge__(self, rhs: Any) -> QueryInstance:
        return self._generate_test(
            lambda value: value >= rhs,
            ('>=', self._path, rhs)
        )

    def exists(self) -> QueryInstance:
        return self._generate_test(
            lambda _: True,
            ('exists', self._path)
        )

    def matches(self, regex: str, flags: int = 0) -> QueryInstance:
        def test(value):
            if not isinstance(value, str):
                return False

            return re.match(regex, value, flags) is not None

        return self._generate_test(test, ('matches', self._path, regex))

    def search(self, regex: str, flags: int = 0) -> QueryInstance:

        def test(value):
            if not isinstance(value, str):
                return False

            return re.search(regex, value, flags) is not None

        return self._generate_test(test, ('search', self._path, regex))

    def test(self, func: Callable[[Mapping], bool], *args) -> QueryInstance:
        return self._generate_test(
            lambda value: func(value, *args),
            ('test', self._path, func, args)
        )

    def any(self, cond: Union[QueryInstance, List[Any]]) -> QueryInstance:
        if callable(cond):
            def test(value):
                return is_sequence(value) and any(cond(e) for e in value)

        else:
            def test(value):
                return is_sequence(value) and any(e in cond for e in value)

        return self._generate_test(
            lambda value: test(value),
            ('any', self._path, freeze(cond))
        )

    def all(self, cond: Union['QueryInstance', List[Any]]) -> QueryInstance:
        if callable(cond):
            def test(value):
                return is_sequence(value) and all(cond(e) for e in value)

        else:
            def test(value):
                return is_sequence(value) and all(e in value for e in cond)

        return self._generate_test(
            lambda value: test(value),
            ('all', self._path, freeze(cond))
        )

    def one_of(self, items: List[Any]) -> QueryInstance:
        return self._generate_test(
            lambda value: value in items,
            ('one_of', self._path, freeze(items))
        )

    def fragment(self, document: Mapping) -> QueryInstance:
        def test(value):
            for key in document:
                if key not in value or value[key] != document[key]:
                    return False

            return True

        return self._generate_test(
            lambda value: test(value),
            ('fragment', freeze(document)),
            allow_empty_path=True
        )

    def noop(self) -> QueryInstance:

        return QueryInstance(
            lambda value: True,
            ()
        )

    def map(self, fn: Callable[[Any], Any]) -> 'Query':
        query = type(self)()
        query._path = self._path + (fn,)
        query._hash = None

        return query


def get(key: str) -> Query:
    return Query()[key]


