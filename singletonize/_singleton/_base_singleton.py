"""Base abstract class for all Singleton implementations."""
from .._metaclasses import SingletonMeta

from typing import Type, TypeVar, Dict, Any

_T = TypeVar('_T', bound='BaseSingleton')

class BaseSingleton():
  """Abstract base class containing common Singleton functionality."""
  __slots__ = ()

  def __setattr__(self, key: str, value: Any) -> None:
    """
    Set an attribute on the singleton instance.

    If the instance is being updated, it allows modification.
    Otherwise, it prevents setting new attributes dynamically.

    :param key: Attribute name
    :param value: Attribute value
    :return None: No return value
    :raises AttributeError: If attempting to set a new attribute after initialization
    """
    if getattr(self, '_updating', False):
      super().__setattr__(key, value)
    elif hasattr(self, key):
      raise AttributeError(f'Cannot set attribute {key} on singleton instance')
    else:
      super().__setattr__(key, value)

  @classmethod
  def get_instance(cls: Type[_T], *args: Any, **kwargs: Any) -> _T:
    """
    Get or create the singleton instance.

    :param args: Positional arguments for instance creation
    :param kwargs: Keyword arguments for instance creation
    :return _T: The singleton instance
    """
    return cls(*args, **kwargs)

  @classmethod
  def has_instance(cls: Type[_T]) -> bool:
    """
    Check if the singleton instance exists.

    :return bool: True if an instance exists, otherwise False
    """
    return SingletonMeta.has_instance(cls)

  @classmethod
  def detach(cls) -> None:
    """
    Remove the singleton instance, allowing a new instance to be created.

    :return None: No return value
    """
    SingletonMeta.detach(cls)

  @classmethod
  def reset_instance(cls: Type[_T], *args: Any, **kwargs: Any) -> _T:
    """
    Reset the singleton instance with new parameters.

    :param args: Positional arguments for new instance creation
    :param kwargs: Keyword arguments for new instance creation
    :return _T: The new singleton instance
    """
    cls.detach()
    return cls.get_instance(*args, **kwargs)

  @classmethod
  def get_instance_or_none(cls: Type[_T]) -> _T | None:
    """
    Return the singleton instance if it exists, otherwise None.

    :return _T: Singleton instance or None if not created
    :return None: No return value
    """
    return SingletonMeta.get_instance_or_none(cls)

  @classmethod
  def is_instance(cls: Type[_T], obj: object) -> bool:
    """
    Check if the given object is the singleton instance.

    :param obj: Object to check
    :return bool: True if the object is the singleton instance, otherwise False
    """
    return isinstance(obj, cls) and obj is cls.get_instance()

  @classmethod
  def update_instance(cls: Type[_T], **kwargs: Any) -> _T:
    """
    Update the singleton instance's attributes with new values.

    :param kwargs: Key-value pairs of attributes to update
    :return: The updated singleton instance
    """
    instance = cls.get_instance()
    instance._updating = True

    try:
      for key, value in kwargs.items():
        setattr(instance, key, value)
    finally:
      instance._updating = False

    return instance

  @classmethod
  def instance_as_dict(cls: Type[_T]) -> Dict[str, Any]:
    """
    Return the singleton instance's attributes as a dictionary, ignoring private attributes.

    :return Dict[str, Any]: Dictionary of instance attributes
    """
    instance = cls.get_instance_or_none()
    return {k: v for k, v in vars(instance).items() if not k.startswith('_')} if instance else {}
