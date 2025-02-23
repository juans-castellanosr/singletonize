import gc
from collections import deque
from typing import Callable, Generator, TypeVar, cast
import types

_NP = (
  types.ModuleType, type, types.FunctionType, types.MethodType,
  types.BuiltinFunctionType, types.BuiltinMethodType,
  types.CodeType, types.LambdaType, types.GeneratorType,
  types.CoroutineType, types.AsyncGeneratorType
)

_T = TypeVar('_T')

class LeanBFS:
  __slots__ = ('max_depth', 'chunk_size', 'queue', 'visited_nodes', 'node_map', 'parent_map', 'iteration')

  def __init__(self, max_depth: int = 100, chunk_size: int = 50):
    self.max_depth = max_depth
    self.chunk_size = chunk_size
    self.reset()

  def _get_children(self, obj: object) -> Generator[object, None, None]:
    """Get all children of an object."""
    if isinstance(obj, dict):
      yield from obj.values()
    elif isinstance(obj, (list, tuple, set, frozenset)):
      yield from obj
    elif hasattr(obj, '__dict__'):
      yield from obj.__dict__.values()
    elif hasattr(obj, '__slots__'):
      yield from (getattr(obj, slot) for slot in getattr(obj, '__slots__', [])  if hasattr(obj, slot))

  def reset(self) -> None:
    """Reset the internal state of the BFS."""
    self.queue: deque[tuple[int, object]] = deque()
    self.visited_nodes: set[int] = set()
    self.node_map: dict[int, object] = {}
    self.parent_map: dict[int, tuple[int, int]] = {}
    self.iteration = 0
    gc.collect()

  def traverse(self, root: object, process_func: Callable[[_T, int], bool]) -> None:
    """Breadth-first traversal of an object graph."""
    self.reset()
    self.queue.append((0, root))
    self.node_map[id(root)] = root

    gc.disable()
    try:
      while self.queue:
        chunk_count = 0

        while self.queue and chunk_count < self.chunk_size:
          iteration, current = self.queue.popleft()
          obj_id = id(current)

          if obj_id in self.visited_nodes:
            continue

          self.visited_nodes.add(obj_id)
          should_continue = process_func(cast(_T, current), iteration)

          if not should_continue or iteration >= self.max_depth:
            continue

          for child in self._get_children(current):
            if (not callable(child) and not isinstance(child, _NP) and isinstance(child, (dict, list, tuple, set, frozenset))):
              new_child = cast(object, child)
              child_id = id(new_child)

              if child_id not in self.node_map:
                self.node_map[child_id] = new_child
                self.iteration += 1
                self.queue.append((self.iteration, new_child))
                self.parent_map[self.iteration] = (iteration, obj_id)

          chunk_count += 1

        if len(self.visited_nodes) > 10000:
          self.visited_nodes = set(list(self.visited_nodes)[-5000:])
          gc.collect()
    finally:
      gc.enable()
      self.reset()

  def get_parent(self, iteration: int) -> (tuple[int, object] | tuple[None, None]):
    """Get the parent of a node by iteration."""
    parent_map = self.parent_map.get(iteration)

    if parent_map:
      parent = self.node_map.get(parent_map[1])
      if parent:
        return parent_map[0], parent

    return None, None
