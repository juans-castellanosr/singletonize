"""Utility module for instance cleanup."""
import gc
from types import ModuleType
from types import FunctionType
from typing import Type, TypeVar, List, Dict, Tuple, Union, Optional, cast

_T = TypeVar('_T')
_RT = List[Union[Dict[str, Optional[_T]], List[Optional[_T]], Tuple[Optional[_T], ...]]]

class InstanceCleaner:
  """Utility class for thorough instance cleanup."""
  @staticmethod
  def cleanup(obj: Optional[Type[_T] | object]) -> None:
    """Clean up an object and its references safely."""
    if obj is None:
      return

    for attr in list(getattr(obj, '__dict__', {})):
      try:
        delattr(obj, attr)
      except (AttributeError, TypeError):
        continue

    referrers = cast(_RT[_T], [
      ref for ref in gc.get_referrers(obj)
      if not isinstance(ref, (type, ModuleType, FunctionType))
    ])

    for ref in referrers:
      if isinstance(ref, dict):
        for k, v in list(ref.items()):
          if v is obj:
            ref[k] = None
      elif isinstance(ref, list):
        for idx, item in enumerate(ref):
          if item is obj:
            ref[idx] = None
      elif isinstance(ref, tuple): #type: ignore
        new_tuple = tuple(item if item is not obj else None for item in ref)
        for referrer in gc.get_referrers(ref):
          if isinstance(referrer, dict):
            for k, v in referrer.items():
              if v is ref:
                referrer[k] = new_tuple
          elif isinstance(referrer, list):
            for idx, item in enumerate(referrer): #type: ignore
              if item is ref:
                referrer[idx] = new_tuple
          elif isinstance(referrer, tuple):
            raise ValueError("Cannot modify tuple referrer")

    gc.collect()