"""Utility module for instance cleanup."""
import gc
from types import ModuleType, FunctionType
from typing import Type, TypeVar, Dict, List, Tuple, Union, Optional, Set, cast, Any

_T = TypeVar("_T")
_R = Union[
  Dict[Any, Optional[_T]],
  List[Optional[_T]],
  Tuple[Optional[_T], ...],
  Set[Optional[_T]]
]

class InstanceCleaner:
  """Utility class for thorough instance cleanup."""
  @staticmethod
  def cleanup(obj: Optional[Type[_T] | object]) -> None:
    """Clean up an object and its references safely."""
    if obj is None:
      return

    InstanceCleaner._clear_attributes(obj)
    InstanceCleaner._clear_references(obj)
    gc.collect()

  @staticmethod
  def _clear_attributes(obj: object) -> None:
    """Remove attributes from an object to release references."""
    if not hasattr(obj, "__dict__"):
      return

    for attr in list(obj.__dict__):
      try:
        delattr(obj, attr)
      except (AttributeError, TypeError):
        pass

  @staticmethod
  def _clear_references(obj: Union[type[_T], object]) -> None:
    """Clear references to an object from referrers."""
    referrers = cast(List[_R[_T]], [
      ref for ref in gc.get_referrers(obj)
      if not isinstance(ref, (type, ModuleType, FunctionType))
    ])

    for ref in referrers:
      InstanceCleaner._clear_container_references(ref, obj)

  @staticmethod
  def _clear_container_references(ref: _R[_T], obj: object) -> None:
    """Remove object references from various container types."""
    if isinstance(ref, dict):
      InstanceCleaner._clear_dict_references(ref, obj)
    elif isinstance(ref, list):
      InstanceCleaner._clear_list_references(ref, obj)
    elif isinstance(ref, tuple):
      InstanceCleaner._clear_tuple_references(ref, obj)

  @staticmethod
  def _clear_dict_references(ref: Dict[Any, Optional[_T]], obj: object) -> None:
    """Remove references from a dictionary."""
    for key in list(ref.keys()):
      if ref[key] is obj:
        ref[key] = None

  @staticmethod
  def _clear_list_references(ref: List[Optional[_T]], obj: object) -> None:
    """Remove references from a list."""
    for idx, item in enumerate(ref):
      if item is obj:
        ref[idx] = None

  @staticmethod
  def _clear_tuple_references(ref: Tuple[Optional[_T], ...], obj: object) -> None:
    """Replace references in a tuple by modifying its referrers."""
    new_tuple = tuple(None if item is obj else item for item in ref)

    for referrer in gc.get_referrers(ref):
      if isinstance(referrer, dict):
        InstanceCleaner._replace_tuple_in_dict(cast(Dict[Any, Optional[_T]], referrer), ref, new_tuple)
      elif isinstance(referrer, list):
        InstanceCleaner._replace_tuple_in_list(cast(List[Optional[_T]], referrer), ref, new_tuple)
      elif isinstance(referrer, tuple):
        raise ValueError("Cannot modify tuple referrer.")

  @staticmethod
  def _replace_tuple_in_dict(referrer: Dict[Any, Any], old_tuple: Tuple[Any, ...], new_tuple: Tuple[Any, ...]) -> None:
    """Replace tuple reference in a dictionary."""
    for key, value in referrer.items():
      if value is old_tuple:
        referrer[key] = new_tuple

  @staticmethod
  def _replace_tuple_in_list(referrer: List[Any], old_tuple: Tuple[Any, ...], new_tuple: Tuple[Any, ...]) -> None:
    """Replace tuple reference in a list."""
    for idx, item in enumerate(referrer):
      if item is old_tuple:
        referrer[idx] = new_tuple
