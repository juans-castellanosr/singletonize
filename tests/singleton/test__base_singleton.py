from singletonize import Singleton

class MySingleton(Singleton):
  def __init__(self, value: int):
    self.value = value

def test_get_instance() -> None:
  MySingleton.detach()

  instance1 = MySingleton.get_instance(1)
  instance2 = MySingleton.get_instance(2)

  assert instance1.value == 1
  assert instance2.value == 1
  assert instance1 is instance2
  assert id(instance1) == id(instance2)

def test_detach() -> None:
  MySingleton.detach()

  MySingleton.get_instance(1)
  assert MySingleton.has_instance()

  MySingleton.detach()
  assert not MySingleton.has_instance()

def test_has_instance() -> None:
  MySingleton.detach()

  assert not MySingleton.has_instance()
  MySingleton.get_instance(1)
  assert MySingleton.has_instance()

def test_reset_instance() -> None:
  MySingleton.detach()

  instance1 = MySingleton.get_instance(1)
  assert instance1.value == 1

  instance2 = MySingleton.reset_instance(2)
  assert instance2.value == 2
  assert instance1 is not instance2

def test_get_instance_or_none() -> None:
  MySingleton.detach()

  assert MySingleton.get_instance_or_none() is None
  instance = MySingleton.get_instance(1)
  assert MySingleton.get_instance_or_none() is instance

def test_is_instance() -> None:
  MySingleton.detach()

  instance = MySingleton.get_instance(1)

  assert MySingleton.is_instance(instance)
  assert not MySingleton.is_instance(object())

def test_update_instance() -> None:
  MySingleton.detach()

  instance = MySingleton.get_instance(1)
  updated_instance = MySingleton.update_instance(value=42)

  assert updated_instance.value == 42
  assert instance is updated_instance

def test_instance_as_dict() -> None:
  MySingleton.detach()

  assert MySingleton.instance_as_dict() == {}

  MySingleton.get_instance(1)
  assert MySingleton.instance_as_dict() == {"value": 1}

def test_multiple_instances() -> None:
  MySingleton.detach()

  instance1 = MySingleton.get_instance(1)
  instance2 = MySingleton.get_instance(1)

  assert instance1 is instance2
  assert id(instance1) == id(instance2)

def test_no_instance_after_detach() -> None:
  MySingleton.detach()

  MySingleton.get_instance(1)
  MySingleton.detach()
  assert MySingleton.get_instance_or_none() is None
