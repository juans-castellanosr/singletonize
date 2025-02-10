import pytest
import gc
from singletonize._utils import InstanceCleaner

class MySingleton:
  def __init__(self) -> None:
    self.attr1 = "value1"
    self.attr2 = "value2"

def test_cleanup_none() -> None:
  InstanceCleaner.cleanup(None)
  assert True

def test_cleanup_object_with_attributes() -> None:
  obj = MySingleton()

  InstanceCleaner.cleanup(obj)
  assert not hasattr(obj, 'attr1')
  assert not hasattr(obj, 'attr2')

def test_cleanup_object_referenced_in_dict() -> None:
  obj = MySingleton()
  ref_dict = {'key': obj}
  InstanceCleaner.cleanup(obj)
  assert ref_dict['key'] is None

def test_cleanup_object_referenced_in_list() -> None:
  obj = MySingleton()
  ref_list = [obj]
  InstanceCleaner.cleanup(obj)
  assert ref_list[0] is None

def test_cleanup_object_referenced_in_tuple() -> None:
  obj = MySingleton()
  container = {"ref": (obj,)}
  InstanceCleaner.cleanup(obj)
  assert container["ref"][0] is None

def test_cleanup_collects_garbage() -> None:
  obj = MySingleton()
  InstanceCleaner.cleanup(obj)
  assert gc.isenabled()

def test_cleanup_object_raising_attribute_error() -> None:
  class FaultyClass:
    def __init__(self) -> None:
      self.attr1 = "value1"
      self.attr2 = "value2"

    def __delattr__(self, name: str) -> None:
      if name == "attr1":
        raise AttributeError("Cannot delete attr1")
      elif name == "attr2":
        raise TypeError("Cannot delete attr2")

  obj = FaultyClass()
  InstanceCleaner.cleanup(obj)

  assert hasattr(obj, "attr1")
  assert hasattr(obj, "attr2")

def test_cleanup_object_without_dict() -> None:
  class NoDictClass:
    __slots__ = ['attr1', 'attr2']

    def __init__(self) -> None:
      self.attr1 = "value1"
      self.attr2 = "value2"

  obj = NoDictClass()
  InstanceCleaner.cleanup(obj)

  assert obj.attr1 == "value1"
  assert obj.attr2 == "value2"

def test_cleanup_object_in_nested_tuple() -> None:
  obj = MySingleton()
  _ = ((obj,),)

  with pytest.raises(ValueError, match="Cannot modify tuple referrer."):
    InstanceCleaner.cleanup(obj)
