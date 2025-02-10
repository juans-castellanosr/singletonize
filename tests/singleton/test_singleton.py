import pytest
from singletonize import Singleton

class MySingleton(Singleton):
  def __init__(self, value: int):
    self.value = value

def test_singleton_instance() -> None:
  test1 = MySingleton(1)
  test2 = MySingleton(2)

  assert test1.value == 1
  assert test2.value == 1
  assert test1 is test2
  assert id(test1) == id(test2)

  with pytest.raises(AttributeError, match='Cannot set attribute value on singleton instance'):
    test1.value = 3
  assert test2.value == test1.value

  with pytest.raises(AttributeError, match='Cannot set attribute value on singleton instance'):
    test1.value = 4
  assert test1.value == test2.value

  assert test1 is test2
  assert id(test1) == id(test2)
