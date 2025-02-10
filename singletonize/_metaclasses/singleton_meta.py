"""Module for Singleton metaclasses implementation."""
from .._utils import InstanceCleaner

from threading import RLock
from typing import Type, TypeVar, Dict, cast, Any
from abc import ABCMeta
from weakref import WeakKeyDictionary, WeakSet

_T = TypeVar('_T')

class SingletonMeta(type):
  """Metaclass for creating Singleton classes."""
  __slots__ = ()
  _instances: WeakKeyDictionary[Type[Any], Any] = WeakKeyDictionary()
  _locks: WeakKeyDictionary[Type[Any], RLock] = WeakKeyDictionary()
  _refs: Dict[Type[Any], WeakSet[Any]] = {}

  def __call__(cls: Type[_T], *args: Any, **kwargs: Any) -> _T:
    """Create or return the singleton instance."""
    if instance := SingletonMeta._instances.get(cls):
      return cast(_T, instance)

    instances = SingletonMeta._instances
    refs = SingletonMeta._refs
    lock = SingletonMeta._locks.setdefault(cls, RLock())

    with lock:
      if cls not in instances:
        instance = super(SingletonMeta, cast(SingletonMeta, cls)).__call__(*args, **kwargs)
        instances[cls] = instance

        if cls not in refs:
          refs[cls] = WeakSet()

        refs[cls].add(instances[cls])

        SingletonMeta._set_del(instance)

      return cast(_T, instances[cls])

  @classmethod
  def _set_del(mcs, cls: Type[_T]) -> None:
    if not hasattr(cls, '__del__'):
      def base_del(self: Type[_T]) -> None:
        SingletonMeta.detach(cast(Type[_T], type(self)))

      setattr(cls, '__del__', base_del.__get__(cls))
    else:
      original_del = getattr(cls, '__del__').__get__(cls)

      def enhanced_del(self: Type[_T]) -> None:
        original_del()
        SingletonMeta.detach(cast(Type[_T], type(self)))

      setattr(cls, '__del__', enhanced_del.__get__(cls))

  @classmethod
  def get_instance_or_none(mcs, cls: Type[_T]) -> _T | None:
    """Get the instance of the Singleton class."""
    return mcs._instances.get(cls)

  @classmethod
  def has_instance(mcs, cls: Type[_T]) -> bool:
    """Check if the Singleton class has an instance."""
    return cls in mcs._instances

  @classmethod
  def detach(mcs, cls: Type[_T]) -> None:
    """Detach the instance of the Singleton class."""
    with mcs._locks.setdefault(cls, RLock()):
      if instance := mcs._instances.get(cls):
        mcs._instances.pop(cls, None)

        if cls in mcs._refs:
          mcs._refs[cls].clear()
          del mcs._refs[cls]

        InstanceCleaner.cleanup(instance)

        mcs._locks.pop(cls, None)

class SingletonABCMeta(SingletonMeta, ABCMeta):
  """Metaclass for creating abstract Singleton classes."""

  __slots__ = ()
