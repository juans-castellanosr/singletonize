import gc
from typing import ValuesView, Iterable, Generator, Callable, Literal, cast
from . import LeanBFS

_CM = dict[str, object] | list[object] | set[object]
_CI = tuple[object, ...] | frozenset[object] | None
_C = _CM | _CI

_NN: tuple[object, ...] = (None, dict(), list(), set(), tuple(), frozenset())

class Cleaner:
  """Utility class for cleaning up objects and their references."""
  max_depth: int = 100
  chunk_size: int = 50
  bfs: LeanBFS | None = None

  @staticmethod
  def reset() -> None:
    """Reset the BFS instance and clean up the references."""
    if Cleaner.bfs:
      Cleaner.bfs.reset()

    Cleaner.max_depth = 100
    Cleaner.chunk_size = 50
    Cleaner.bfs = None
    gc.collect()

  @staticmethod
  def _clean_references(obj: object, new_obj: _CI = None) -> Callable[[_C, int], Literal[True]]:
    """Process all referrers of an object and clean references to the object."""
    def clean_references(ref: _C, iteration: int) -> Literal[True]:
      """Process referrers of an object."""
      try:
        Cleaner._process_referrers(ref, (obj,), new_obj)
        return True
      except Exception as e:
        raise Exception(f"Error processing referrers: {e}")

    return clean_references

  @staticmethod
  def _clean_empty_objects(ref: _C, iteration: int) -> Literal[True]:
    """Clean empty objects."""
    try:
      if ref in _NN:
        Cleaner._process_parent(iteration)
        return True

      Cleaner._process_referrers(ref, _NN)

      if ref in _NN:
        Cleaner._process_parent(iteration)

      return True
    except Exception as e:
      raise RuntimeError(f"Error cleaning empty objects: {e}")

  @staticmethod
  def _process_referrers(ref: _C, objs: tuple[object, ...], new_obj: _CI = None) -> None:
    """Clean references to the target objects."""
    if Cleaner._contains_instance(ref):
      return

    if isinstance(ref, dict):
      keys_to_remove: list[str] = []

      for key, value in ref.items():
        if value in objs:
          if new_obj:
            ref[key] = new_obj
          else:
            keys_to_remove.append(key)

        if key in objs:
          keys_to_remove.append(key)

      for key in keys_to_remove:
        ref.pop(key, None)
    elif isinstance(ref, list):
      if new_obj:
        ref[:] = [new_obj if item in objs else item for item in ref]
      else:
        ref[:] = [item for item in ref if item not in objs]
    elif isinstance(ref, set):
      ref -= {item for item in ref if item in objs}
      if new_obj:
        ref.add(new_obj)
    elif isinstance(ref, (tuple, frozenset)):
      new_ref = new_obj or ref
      process_item = Cleaner._process_item(objs, new_obj)
      cleaned_ref = type(ref)(process_item(item) for item in new_ref if item not in objs)

      for container in gc.get_referrers(ref):
        Cleaner._process_referrers(container, (ref,), cleaned_ref)

  @staticmethod
  def _contains_instance(ref: _C) -> bool:
    """Check if the reference contains an instance of the target types."""
    target_types = (Cleaner, LeanBFS)
    values: Iterable[object] | ValuesView[object] | None = None

    if isinstance(ref, dict):
      values = ref.values()
    elif isinstance(ref, (list, set, tuple, frozenset)):
      values = ref
    else:
      return False

    return any(isinstance(item, target_types) for item in values)

  @staticmethod
  def _process_parent(iteration: int) -> None:
    """Clean the parent object if necessary."""
    if Cleaner.bfs is None:
      raise Exception("BFS instance is not initialized yet")

    iteration_parent, parent = Cleaner.bfs.get_parent(iteration)
    if parent is not None and iteration_parent is not None:
      Cleaner._clean_empty_objects(cast(_C, parent), iteration_parent)

  @staticmethod
  def _process_item(objs: tuple[object, ...], new_obj: _CI = None) -> Callable[[object], object]:
    """Process an item and its references."""
    def process_item(item: object) -> (_CI | object):
      """Process an item and its references."""
      if isinstance(item, (tuple, frozenset)):
        new_item = cast(tuple[object, ...] | frozenset[object], item)
        return type(new_item)(cast(Generator[_CI, None, None], (process_item(sub) for sub in new_item if sub not in objs)))
      return new_obj if item in objs else item

    return process_item

  @staticmethod
  def cleanup(obj: object, max_depth: int = 100, chunk_size: int = 50) -> None:
    """Clean up an object and its references."""
    Cleaner.reset()

    if not obj:
      return

    if hasattr(obj, "__dict__"):
      obj.__dict__.clear()

    Cleaner.max_depth = max_depth
    Cleaner.chunk_size = chunk_size

    Cleaner.bfs = LeanBFS(Cleaner.max_depth, Cleaner.chunk_size)

    referrers = gc.get_referrers(obj)
    Cleaner.bfs.traverse(referrers, Cleaner._clean_references(obj))
    Cleaner.bfs.traverse(referrers, Cleaner._clean_empty_objects)

    referrers.clear()
    Cleaner.reset()
