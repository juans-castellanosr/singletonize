import re
import pytest
from singletonize import SingletonABC

class MySingletonABC(SingletonABC):
  def __init__(self, value: int):
    self.value = value

def test_singleton_abc_instance() -> None:
  test1 = MySingletonABC(1)
  test2 = MySingletonABC(2)

  assert test1.value == 1
  assert test2.value == 1
  assert test1 is test2
  assert id(test1) == id(test2)

  with pytest.raises(AttributeError, match=re.escape("Cannot set attribute 'value' on immutable singleton instance. Use update_instance() to modify existing attributes.")):
    test1.value = 3

  assert test2.value == test1.value

  with pytest.raises(AttributeError, match=re.escape("Cannot set attribute 'value' on immutable singleton instance. Use update_instance() to modify existing attributes.")):
    test1.value = 4

  assert test1.value == test2.value

  assert test1 is test2
  assert id(test1) == id(test2)
  