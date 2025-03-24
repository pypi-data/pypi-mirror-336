from __future__ import annotations

from collections import defaultdict
from operator import itemgetter
from typing import Any, Hashable, Iterable, Iterator, Protocol, Self, Sized, overload, Union, MutableMapping, runtime_checkable


_BUGREPORT_MSG: str = "Please file a bugreport if ypu have not fiddled with any internal fields or methods of OrderedMultiDict."
_DESYNCED_ERROR_MSG: str = f"OrderedMultiDict._items and OrderedMultiDict._map have de-synced. {_BUGREPORT_MSG}"
_EMPTY_DEQUE_ERROR_MSG: str = f"OrderedMultiDict._map contained an empty deque. OrderedMultiDict._items and OrderedMultiDict._map might have de-synced. {_BUGREPORT_MSG}"

_SENTINEL = object()
_SENTINEL2 = object()


@runtime_checkable
class _SupportsKeysAndGetItem[TK: Hashable, TV](Protocol):
	def keys(self) -> Iterable[TK]: ...
	def __getitem__(self, key: TK, /) -> TV: ...


@runtime_checkable
class _SizedIterable[T](Iterable[T], Sized, Protocol):
	...


def _pop_first[TK: Hashable, TV](d: dict[TK, TV]) -> tuple[TK, TV]:
	return (k := next(iter(d)), d.pop(k))


def _pop_last[TK: Hashable, TV](d: dict[TK, TV]) -> tuple[TK, TV]:
	return d.popitem()


def _iter_keys[TK](values: Iterable[tuple[TK, Any]]) -> Iterator[TK]:
	return map(itemgetter(0), values)


def _iter_values[TV](values: Iterable[tuple[Any, TV]]) -> Iterator[TV]:
	return map(itemgetter(1), values)


class MultiDict[TK: Hashable, TV](MutableMapping[TK, TV]):
	# _ItemsDictCls: ClassVar[Type[dict]]
	# _DequeCls: ClassVar[Type[Iterable]]

	# def _items_pop_first(self, items: dict) -> tuple[int, tuple[TK, TV]]:
	# 	raise NotImplementedError('_items_pop_first()')

	def _q_popleft(self, que) -> TV:
		# raise NotImplementedError('_q_popleft()')
		return que.pop(0)

	@overload
	def __init__(self) -> None: ...
	@overload
	def __init__(self, __map: _SupportsKeysAndGetItem[TK, TV], /) -> None: ...
	@overload
	def __init__(self, __iterable: Iterable[tuple[TK, TV]], /) -> None: ...
	@overload
	def __init__(self: MultiDict[str, TV], /, **kwargs: TV) -> None: ...
	@overload
	def __init__(self: MultiDict[str, TV], /, __map: _SupportsKeysAndGetItem[str, TV], **kwargs: TV) -> None: ...
	@overload
	def __init__(self: MultiDict[str, TV], /, __iterable: Iterable[tuple[str, TV]], **kwargs: TV) -> None: ...

	# Next two overloads are for OrderedMultiDict(string.split(sep) for string in iterable)
	# Cannot be Iterable[Sequence[_T]] or otherwise dict(["foo", "bar", "baz"]) is not an error
	@overload
	def __init__(self: MultiDict[str, str], __iterable: Iterable[list[str]], /) -> None: ...
	@overload
	def __init__(self: MultiDict[bytes, bytes], __iterable: Iterable[list[bytes]], /) -> None: ...

	def __init__(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV] = _SENTINEL, /, **kwargs: TV):
		self._map: defaultdict[TK, list[TV]] = defaultdict(list)
		self._len: int = 0

		if iterable_or_map is not _SENTINEL:
			self._load(iterable_or_map)
		if kwargs:
			self._extend_fast(kwargs.items())

	def _load(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV]):
		"""
		Clear all existing key:value items and import all key:value items from
		<mapping>. If multiple values exist for the same key in <mapping>, they
		are all be imported.
		"""
		if isinstance(iterable_or_map, MultiDict):
			self._copy_from(iterable_or_map)  # special case
		else:
			self.clear()
			self._extend(iterable_or_map)

	@overload
	def update(self, __m: _SupportsKeysAndGetItem[TK, TV], /) -> None: ...
	@overload
	def update(self, __m: Iterable[tuple[TK, TV]], /) -> None: ...
	@overload
	def update(self: MultiDict[str, TV], /, **kwargs: TV) -> None: ...
	@overload
	def update(self: MultiDict[str, TV], __m: _SupportsKeysAndGetItem[str, TV], /, **kwargs: TV) -> None: ...
	@overload
	def update(self: MultiDict[str, TV], __m: Iterable[tuple[str, TV]], /, **kwargs: TV) -> None: ...

	def update(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV] = _SENTINEL, /, **kwargs: TV):
		"""
		Clear all existing key:value entries that have a key which is present in <iterable_or_map>. And then import all
		key:value items from <iterable_or_map>. If multiple values exist for the same key in <mapping>, they are all
		imported. Keys that are not present in <iterable_or_map> are not touched.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3)])
			>>> omd.update([(1, '1'), (3, '3'), (1, '11')])
			>>> print(omd.items())    # _ItemsView([(2, 2), (2, 22), (1, '1'), (3, '3'), (1, '11')])
		"""

		if iterable_or_map is not _SENTINEL:
			self._try_delete_all_keys(iterable_or_map)
		if kwargs:
			self._try_delete_all_keys(kwargs)

		self.extend(iterable_or_map, **kwargs)

	def _try_delete_all_keys(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV]):
		if hasattr(iterable_or_map, 'unique_keys'):  # support for OrderedMultiDict
			for k in iterable_or_map.unique_keys():
				self._try_delete_all(k)
		elif hasattr(iterable_or_map, 'keys'):
			for k in iterable_or_map.keys():
				self._try_delete_all(k)
		elif hasattr(iterable_or_map, 'items'):
			for k in dict.fromkeys(_iter_keys(iterable_or_map.items)):
				self._try_delete_all(k)
		else:
			for k in dict.fromkeys(_iter_keys(iterable_or_map)):
				self._try_delete_all(k)

	@overload
	def extend(self, __m: _SupportsKeysAndGetItem[TK, TV], /) -> None: ...
	@overload
	def extend(self, __m: Iterable[tuple[TK, TV]], /) -> None: ...
	@overload
	def extend(self: MultiDict[str, TV], /, **kwargs: TV) -> None: ...
	@overload
	def extend(self: MultiDict[str, TV], __m: _SupportsKeysAndGetItem[str, TV], /, **kwargs: TV) -> None: ...
	@overload
	def extend(self: MultiDict[str, TV], __m: Iterable[tuple[str, TV]], /, **kwargs: TV) -> None: ...

	def extend(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV] = _SENTINEL, /, **kwargs: TV):
		"""
		Adds all key:value items from <iterable_or_map>. If multiple values exist for the same key in <mapping>, they are all
		imported.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3)])
			>>> omd.extend([(1, '1'), (3, '3'), (1, '11')])
			>>> print(omd.items())    # _ItemsView([(1,1), (2,2), (1,11), (2, 22), (3,3), (1, '1'), (3, '3'), (1, '11')])
		"""
		if iterable_or_map is not _SENTINEL:
			self._extend(iterable_or_map)
		if kwargs:
			self._extend(kwargs)

	def _extend(self, iterable_or_map: Iterable[tuple[TK, TV]] | _SupportsKeysAndGetItem[TK, TV]):
		if hasattr(iterable_or_map, 'items'):
			self._extend_fast(iterable_or_map.items())
		elif isinstance(iterable_or_map, _SupportsKeysAndGetItem):
			for k, in iterable_or_map.keys():
				self.add(k, iterable_or_map[k])
			#elif hasattr(iterable_or_map, '__len__') and hasattr(iterable_or_map, '__iter__'):
		elif isinstance(iterable_or_map, _SizedIterable):
			self._extend_fast(iterable_or_map)
		else:
			self._extend_slow(iterable_or_map)

	def _extend_fast(self, items: _SizedIterable[tuple[TK, TV]]) -> None:
		s_map = self._map
		try:
			for it0, it1 in items:
				s_map[it0].append(it1)  # entry in _map is created here if necessary, because _map is a defaultdict
		except:
			self._recalculate_length()
			raise
		else:
			self._len += len(items)

	def _extend_slow(self, items) -> None:
		s_map = self._map
		i = 0
		try:
			for i, (k, v) in enumerate(items, 1):
				# entry in _map is created here if necessary, because _map is a defaultdict
				s_map[k].append(v)
		finally:
			self._len += i

	def _recalculate_length(self) -> None:
		self._len = sum(map(len, self._map.values()))

	def _copy_from(self, other: MultiDict[TK, TV]) -> Self:
		self._map = defaultdict(list, {key: list(que) for key, que in other._map.items()})
		self._len = other._len
		return self

	def copy(self) -> Self:
		return type(self)()._copy_from(self)

	def clear(self):
		self._map.clear()
		self._len = 0

	def _get_all_or_none(self, key: TK) -> list[TV] | None:
		result = self._map.get(key)
		if result is not None:  # if key in self:
			assert result, _EMPTY_DEQUE_ERROR_MSG  # result must not be empty!
			return result
		else:
			return None

	def get[TT](self, key: TK, default: TT = None) -> TV | TT:
		""" same as getlast(...)
		"""
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return values[-1]
		return default

	def getfirst[TT](self, key, default: TT = None) -> TV | TT:
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return values[0]
		return default

	def getlast[TT](self, key: TK, default: TT = None) -> TV | TT:
		""" same as get(...)
		"""
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return values[-1]
		return default

	@overload
	def getall(self, key: TK) -> list[TV]:
		"""
		Returns: The list of values for <key> if <key> is in the dictionary,
		else <default>. If <default> is not provided, an empty list is
		returned.
		"""
		...

	@overload
	def getall[TT](self, key: TK, default: TT) -> list[TV] | TT:
		"""
		Returns: The list of values for <key> if <key> is in the dictionary,
		else <default>. If <default> is not provided, an empty list is
		returned.
		"""
		...

	def getall[TT](self, key: TK, default: TT = _SENTINEL) -> list[TV] | TT:
		"""
		Returns: The list of values for <key> if <key> is in the dictionary,
		else <default>. If <default> is not provided, an empty list is
		returned.
		"""
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return [v for v in values]
		elif default is _SENTINEL:
			return []
		else:
			return default

	def setdefault(self, key: TK, /, default: TV) -> TV:
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return values[-1]
		self.add(key, default)
		return default

	def setdefaultall(self, key: TK, defaultlist: list[TV]) -> list[TV]:
		"""
		Similar to setdefault() except <defaultlist> is a list of values to set
		for <key>. If <key> already exists, its existing list of values is
		returned.

		If <key> isn't a key and <defaultlist> is an empty list, [], no values
		are added for <key> and <key> will not be added as a key.

		Returns: List of <key>'s values if <key> exists in the dictionary,
		otherwise <defaultlist>.
		"""
		if (values := self.getall(key, _SENTINEL2)) is not _SENTINEL2:
			return values
		self.addall(key, defaultlist)
		return defaultlist

	def setall(self, key: TK, value_list: list[TV]) -> None:
		self._try_delete_all(key)
		self.addall(key, value_list)

	def add(self, key: TK, value: TV) -> None:
		"""
		Add <value> to the list of values for <key>. If <key> is not in the
		dictionary, then <value> is added as the sole value for <key>.

		Example:
			>>> omd = OrderedMultiDict()
			>>> omd.add(1, 1)   # list(omd.items()) == [(1,1)]
			>>> omd.add(1, 11)  # list(omd.items()) == [(1,1), (1,11)]
			>>> omd.add(2, 2)   # list(omd.items()) == [(1,1), (1,11), (2,2)]
			>>> omd.add(1, 111) # list(omd.items()) == [(1,1), (1,11), (2,2), (1, 111)]

		Returns: <self>.
		"""
		self._map[key].append(value)  # entry in _map is created here if necessary, because _map is a defaultdict:
		self._len += 1

	def addall(self, key: TK, value_list: list[TV]) -> None:
		"""
		Add the values in <valueList> to the list of values for <key>. If <key>
		is not in the dictionary, the values in <valueList> become the values
		for <key>.

		Example:
			>>> omd: OrderedMultiDict[int, int | str] = OrderedMultiDict([(1,1)])
			>>> omd.addall(1, [11, 111]) # list(omd.items()) == [(1, 1), (1, 11), (1, 111)]
			>>> omd.addall(2, [2])       # list(omd.items()) == [(1, 1), (1, 11), (1, 111), (2, 2)]
			>>> omd.addall(1, ['one'])   # list(omd.items()) == [(1, 1), (1, 11), (1, 111), (2, 2), (1, 'one')]

		Returns: <self>.
		"""
		if not value_list:
			return
		self._map[key].extend(value_list)
		self._len += len(value_list)

	@overload
	def popall(self, key: TK, /) -> Union[list[TV]]:
		"""
		If <key> is in the dictionary, pop it and return its list of values. If
		<key> is not in the dictionary, return <default>. KeyError is raised if
		<default> is not provided and <key> is not in the dictionary.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.popall(2))  # [2, 22]
			>>> print(omd.items())    # _ItemsView([(1, 1), (1, 11), (3,3), (1, 111)])
			>>> print(omd.popall(1))  # [1, 11, 111]
			>>> print(omd.items())    # _ItemsView([(3,3)])
			>>> omd.popall(1)         # raises KeyError

		Raises: KeyError if <key> is absent in the dictionary and <default> isn't
			provided.
		Returns: List of <key>'s values.
		"""
		...

	@overload
	def popall[TT](self, key: TK, /, default: TT) -> list[TV] | TT:
		"""
		If <key> is in the dictionary, pop it and return its list of values. If
		<key> is not in the dictionary, return <default>. KeyError is raised if
		<default> is not provided and <key> is not in the dictionary.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.popall(2, None))  # [2, 22]
			>>> print(omd.items())          # _ItemsView([(1, 1), (1, 11), (3,3), (1, 111)])
			>>> print(omd.popall(1, None))  # [1, 11, 111]
			>>> print(omd.items())          # _ItemsView([(3,3)])
			>>> print(omd.popall(1, None))  # None

		Raises: KeyError if <key> is absent in the dictionary and <default> isn't
			provided.
		Returns: List of <key>'s values.
		"""
		...

	def popall[TT](self, key: TK, /, default: TT = _SENTINEL) -> list[TV] | TT:
		"""
		If <key> is in the dictionary, pop it and return its list of values. If
		<key> is not in the dictionary, return <default>. KeyError is raised if
		<default> is not provided and <key> is not in the dictionary.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.popall(2))  # [2, 22]
			>>> print(omd.items())    # _ItemsView([(1, 1), (1, 11), (3,3), (1, 111)])
			>>> print(omd.popall(1))  # [1, 11, 111]
			>>> print(omd.items())    # _ItemsView([(3,3)])

		Raises: KeyError if <key> is absent in the dictionary and <default> isn't
			provided.
		Returns: List of <key>'s values.
		"""
		if (values := self._map.pop(key, None)) is not None:
			self._len -= len(values)
			return values
		elif default is not _SENTINEL:
			return default
		raise KeyError(key)

	@overload
	def popfirstitem(self) -> tuple[TK, TV]:
		""" """
		...

	@overload
	def popfirstitem[TT](self, *, default: TT) -> tuple[TK, TV] | TT:
		""" """
		...

	def popfirstitem[TT](self, *, default: TT = _SENTINEL) -> tuple[TK, TV] | TT:
		return self._popitem(default, last=False)

	@overload
	def poplastitem(self) -> tuple[TK, TV]:
		""" """
		...

	@overload
	def poplastitem[TT](self, *, default: TT) -> tuple[TK, TV] | TT:
		""" """
		...

	def poplastitem[TT](self, *, default: TT = _SENTINEL) -> tuple[TK, TV] | TT:
		return self._popitem(default, last=True)

	def _popitem[TT](self, default: TT, *, last: bool) -> tuple[TK, TV] | TT:
		try:
			key, values = next(reversed(self._map.items())) if last else next(iter(self._map.items()))
		except (StopIteration, KeyError):
			if default is not _SENTINEL:
				return default
			raise KeyError("dictionary is empty") from None

		assert values, _DESYNCED_ERROR_MSG
		value = values.pop() if last else self._q_popleft(values)
		if not values:
			del self._map[key]
		self._len -= 1
		return key, value

	@overload
	def popfirst(self, key: TK, /) -> TV:
		"""
		Raises: KeyError if <key> is absent.
		"""
		pass

	@overload
	def popfirst[TT](self, key: TK, /, default: TT) -> TV | TT:
		"""
		returns default if <key> is absent.
		"""
		pass

	def popfirst[TT](self, key: TK, /, default: TT = _SENTINEL) -> TV | TT:
		return self._pop(key, default, last=False)

	@overload
	def poplast(self, key: TK, /) -> TV:
		"""

		Raises: KeyError if <key> is absent.
		"""
		pass

	@overload
	def poplast[TT](self, key: TK, /, default: TT) -> TV | TT:
		"""
		returns default if <key> is absent.
		"""
		pass

	def poplast[TT](self, key: TK, /, default: TT = _SENTINEL) -> TV | TT:
		"""
		"same as .pop(...)"
		"""
		return self._pop(key, default, last=True)

	@overload
	def pop(self, key: TK, /) -> TV: ...
	@overload
	def pop(self, key: TK, /, default: TV) -> TV: ...
	@overload
	def pop[TT](self, key: TK, /, default: TT) -> TV | TT: ...

	def pop[TT](self, key: TK, /, default: TT = _SENTINEL) -> TV | TT:
		return self._pop(key, default, last=True)

	def _pop[TT](self, key: TK, default: TT, *, last: bool) -> TV | TT:
		if (values := self._map.get(key)) is not None:
			assert values, _DESYNCED_ERROR_MSG
			popped = values.pop() if last else self._q_popleft(values)
			if not values:
				del self._map[key]
			self._len -= 1
			return popped
		elif default is not _SENTINEL:
			return default
		raise KeyError(key)

	def delete_all(self, key: TK) -> None:
		"""
		Removes all entries for key. Raises a KeyError if key is not in the dictionary.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> omd.delete_all(1)
			>>> print(omd.items())  # _ItemsView([(2,2), (3,3)])
			>>> omd.delete_all(99)  # raises KeyError
		"""
		if not self._try_delete_all(key):
			raise KeyError(key)

	def _try_delete_all(self, key: TK) -> bool:
		"""
		Removes all entries for key.
		Returns True if key was in the dictionary, otherwise False.
		"""
		if (values := self._map.pop(key, None)) is not None:
			self._len -= len(values)
			return True
		return False

	def items(self) -> _ItemsView[TK, TV]:
		"""
		Returns: An ItemsView of all (key, value) pairs in insertion order.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.items())  # _ItemsView([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
		"""
		return _ItemsView(self)

	def keys(self) -> _KeysView[TK, TV]:
		"""
		Returns: A KeysView of all keys in insertion order. Keys can appear multiple times.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.keys())  # _KeysView([1, 2, 1, 2, 3, 1])
		"""
		return _KeysView(self)

	def unique_keys(self) -> _UniqueKeysView[TK, TV]:
		"""
		Returns: A KeysView of all unique keys in order of first appearance. Keys only appear once.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.unique_keys())  # _UniqueKeysView([1, 2, 3])
		"""
		return _UniqueKeysView(self)

	def values(self) -> _ValuesView[TV, TV]:
		"""
		Returns: A ValuesView of all values in insertion order.

		Example:
			>>> omd = OrderedMultiDict([(1,1), (2,2), (1,11), (2, 22), (3,3), (1,111)])
			>>> print(omd.values())  # _ValuesView([1, 2, 11, 22, 3, 111])
		"""
		return _ValuesView(self)

	# def sort(self, *, key: Optional[Callable[[tuple[TK, TV]], Any]] = None, reverse: bool = False):
	# 	self._items = dict(enumerate(sorted(self._items.values(), key=key, reverse=reverse)))
	# 	todo: update self._map
	# 	self._index = len(self._items)

	def contains_item(self, key: TK, value: TV) -> bool:
		if (values := self._map.get(key)) is not None:
			return value in values
		return False

	def contains_value(self, value: TV) -> bool:
		# the same implementation as in _ValuesView.__contains__()
		return any(value in values for values in self._map.values())

	def __eq__(self, other) -> bool:
		if type(self) is not type(other):
			return NotImplemented
		if self._len != other._len:
			return False
		return self._map == other._map
		# return all(map(eq, self._items.values(), other._items.values()))

	def __ne__(self, other) -> bool:
		return not self.__eq__(other)

	def __len__(self) -> int:
		return self._len

	def __iter__(self) -> Iterator[TK]:
		return iter(self.keys())

	def __contains__(self, key: TK) -> bool:
		return self._map.__contains__(key)

	def __getitem__(self, key: TK) -> TV:
		if (values := self._get_all_or_none(key)) is not None:  # if key in self:
			return values[-1]
		raise KeyError(key)

	def __setitem__(self, key: TK, value: TV) -> None:
		self.setall(key, [value])

	def __delitem__(self, key: TK) -> None:
		self.pop(key)

	def __bool__(self) -> bool:
		return bool(self._map)

	def __str__(self) -> str:
		return '{%s}' % ', '.join(f'{key!r}: {values!r}' for key, values in self._map.items())

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({list(self._map.items())!r})'

	def __getstate__(self) -> list[tuple[TK, list[TV]]]:
		return list(self._map.items())

	def __setstate__(self, state: list[tuple[TK, list[TV]]]):
		self._load(state)


class _ViewBase[TK: Hashable, TV]:

	def __init__(self, impl: MultiDict[TK, TV]):
		self._impl: MultiDict[TK, TV] = impl
		self._map: dict[TK, list[TV]] = impl._map

	def __len__(self):
		return self._impl._len

	def __iter__(self) -> Iterator[Any]:
		raise NotImplementedError(f"{type(self).__name__}.__iter__()")

	def __reversed__(self) -> Iterator[Any]:
		raise NotImplementedError(f"{type(self).__name__}.__reversed__()")

	def __repr__(self):
		return f'{type(self).__name__}({list(self)})'


class _ItemsView[TK: Hashable, TV](_ViewBase[TK, TV]):

	def __contains__(self, item: tuple[TK, TV]) -> bool:
		if not isinstance(item, tuple) or len(item) != 2:
			return False
		return self._impl.contains_item(*item)

	def __iter__(self) -> Iterator[tuple[TK, TV]]:
		for k, vs in self._map.items():
			yield from ((k, v) for v in vs)

	def __reversed__(self) -> Iterator[tuple[TK, TV]]:
		for k, vs in reversed(self._map):
			yield from ((k, v) for v in reversed(vs))


class _ValuesView[TV](_ViewBase[Any, TV]):

	def __contains__(self, value: TV) -> bool:
		return any(value in values for values in self._map.values())

	def __iter__(self) -> Iterator[TV]:
		for k, vs in self._map.items():
			yield from vs

	def __reversed__(self) -> Iterator[TV]:
		for k, vs in reversed(self._map):
			yield from reversed(vs)


class _KeysView[TK: Hashable](_ViewBase[TK, Any]):

	def __contains__(self, key: TK) -> bool:
		return self._impl.__contains__(key)

	def __iter__(self) -> Iterator[TK]:
		for k, vs in self._map.items():
			yield from (k for _ in vs)

	def __reversed__(self) -> Iterator[TK]:
		for k, vs in reversed(self._map):
			yield from (k for _ in vs)


class _UniqueKeysView[TK: Hashable](_ViewBase[TK, Any]):

	def __contains__(self, key: TK) -> bool:
		return self._impl.__contains__(key)

	def __iter__(self) -> Iterator[TK]:
		# we cannot iterate over self._impl._map, because its order might not be up-to-date.
		return iter(self._map)

	def __reversed__(self) -> Iterator[TK]:
		# we cannot iterate over self._impl._map, because its order might not be up-to-date.
		return reversed(self._map)

	def __len__(self):
		return len(self._map)


__all__ = ['MultiDict']
