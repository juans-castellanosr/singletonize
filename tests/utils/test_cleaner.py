import gc
from singletonize._utils import Cleaner

class MySingleton:
  def __init__(self) -> None:
    self.attr1 = "value1"
    self.attr2 = "value2"

def test_cleanup_none() -> None:
  Cleaner.cleanup(None)
  assert True

def test_cleanup_object_with_attributes() -> None:
  obj = MySingleton()

  Cleaner.cleanup(obj)
  assert not hasattr(obj, 'attr1')
  assert not hasattr(obj, 'attr2')

def test_cleanup_object_referenced_in_dict() -> None:
  obj = MySingleton()
  ref_dict = {'key': obj}
  Cleaner.cleanup(obj)
  assert ref_dict == {}

def test_cleanup_object_referenced_in_list() -> None:
  obj = MySingleton()
  ref_list = [obj]
  Cleaner.cleanup(obj)
  assert ref_list == []

def test_cleanup_object_referenced_in_tuple() -> None:
  obj = MySingleton()
  container = {"ref": (obj,)}
  Cleaner.cleanup(obj)
  assert container == {}

def test_cleanup_collects_garbage() -> None:
  obj = MySingleton()
  Cleaner.cleanup(obj)
  assert gc.isenabled()

def test_cleanup_object_raising_attribute_error() -> None:
  class FaultyClass:
    def __init__(self) -> None:
      self.attr1 = "value1"
      self.attr2 = "value2"

  obj = FaultyClass()
  Cleaner.cleanup(obj)

  assert not hasattr(obj, "attr1")
  assert not hasattr(obj, "attr2")

def test_cleanup_object_without_dict() -> None:
  class NoDictClass:
    __slots__ = ['attr1', 'attr2']

    def __init__(self) -> None:
      self.attr1 = "value1"
      self.attr2 = "value2"

  obj = NoDictClass()
  Cleaner.cleanup(obj)

  assert obj.attr1 == "value1"
  assert obj.attr2 == "value2"

def test_cleanup_object_in_nested_tuple() -> None:
  obj = MySingleton()
  _ = (obj,)

  Cleaner.cleanup(obj)

  assert _ == (obj,)

def test_cleanup_object_referenced_in_nested_dict() -> None:
  obj = MySingleton()
  nested_dict = {'outer': {'inner': obj}}
  Cleaner.cleanup(obj)
  assert nested_dict['outer'] == {}

def test_cleanup_object_referenced_in_nested_list() -> None:
  obj = MySingleton()
  nested_list = [[obj]]
  Cleaner.cleanup(obj)
  assert nested_list[0] == []

def test_cleanup_object_referenced_in_nested_tuple() -> None:
  obj = MySingleton()
  _ = ((obj,),)
  Cleaner.cleanup(obj)

  assert _ == ((obj,),)

def test_cleanup_object_referenced_in_mixed_container() -> None:
  obj = MySingleton()
  mixed_container = {'key': [obj]}
  Cleaner.cleanup(obj)
  assert mixed_container['key'] == []

def test_cleanup_object_referenced_in_self_referencing_dict() -> None:
  obj = MySingleton()
  self_ref_dict = {'key': obj}
  self_ref_dict['self'] = self_ref_dict #type: ignore
  Cleaner.cleanup(obj)
  assert self_ref_dict == {'self': self_ref_dict} #type: ignore

def test_cleanup_object_referenced_in_self_referencing_list() -> None:
  obj = MySingleton()
  self_ref_list = [obj]
  self_ref_list.append([obj]) #type: ignore
  Cleaner.cleanup(obj)
  assert self_ref_list == []

def test_cleanup_object_referenced_in_self_referencing_tuple() -> None:
  obj = MySingleton()
  self_ref_tuple = (obj,)
  self_ref_tuple = (self_ref_tuple,) #type: ignore
  Cleaner.cleanup(obj)

  assert self_ref_tuple == ((obj,),) #type: ignore
