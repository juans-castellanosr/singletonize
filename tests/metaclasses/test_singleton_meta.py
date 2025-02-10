from singletonize._metaclasses import SingletonMeta, SingletonABCMeta

class MySingleton(metaclass=SingletonMeta):
  def __init__(self, value: int):
    self.value = value

  def __del__(self) -> None:
    if hasattr(self, 'value'):
      del self.value

class MySingletonABC(metaclass=SingletonABCMeta):
  def __init__(self, value: int):
    self.value = value

  def __del__(self) -> None:
    if hasattr(self, 'value'):
      del self.value

class NoDelSingleton(metaclass=SingletonMeta):
  def __init__(self, value: int):
    self.value = value

class NoDelSingletonABC(metaclass=SingletonABCMeta):
  def __init__(self, value: int):
    self.value = value

def test_singleton_instance_creation() -> None:
  SingletonMeta.detach(MySingleton)

  value = 1

  instance1 = MySingleton(value)
  instance2 = MySingleton(2)

  assert instance1 is instance2
  assert instance1.value == value
  assert instance2.value == value

def test_singleton_get_instance() -> None:
  SingletonMeta.detach(MySingleton)

  instance1 = SingletonMeta.get_instance_or_none(MySingleton)

  assert instance1 is None

  MySingleton(1)

  instance2 = SingletonMeta.get_instance_or_none(MySingleton)

  assert instance2 is not None

  assert instance2.value == 1

def test_singleton_instance_modification() -> None:
  SingletonMeta.detach(MySingleton)

  instance1 = MySingleton(1)
  instance2 = MySingleton(2)

  instance1.value = 3
  assert instance2.value == instance1.value

  instance2.value = 4
  assert instance1.value == instance2.value

def test_singleton_instance_deletion() -> None:
  SingletonMeta.detach(MySingleton)

  instance1 = MySingleton(1)
  assert SingletonMeta.has_instance(MySingleton)

  SingletonMeta.detach(MySingleton)
  assert not SingletonMeta.has_instance(MySingleton)

  assert MySingleton not in SingletonMeta._refs #type: ignore
  assert MySingleton not in SingletonMeta._locks #type: ignore

  instance2 = MySingleton(2)
  assert instance1 is not instance2
  assert instance2.value == 2

def test_singleton_instance_without_del() -> None:
  SingletonMeta.detach(MySingleton)

  instance1 = NoDelSingleton(1)
  assert hasattr(instance1, "__del__")

  instance1.__del__() #type: ignore

  assert not SingletonMeta.has_instance(NoDelSingleton)

def test_singleton_instance_with_existing_del() -> None:
  SingletonMeta.detach(MySingleton)

  instance1 = MySingleton(1)
  assert hasattr(instance1, "__del__")

  instance1.__del__()

  assert not SingletonMeta.has_instance(MySingleton)

def test_singleton_abc_instance_creation() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  value = 1

  instance1 = MySingletonABC(value)
  instance2 = MySingletonABC(2)

  assert instance1 is instance2
  assert instance1.value == value
  assert instance2.value == value

def test_singleton_abc_get_instance() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  instance1 = SingletonABCMeta.get_instance_or_none(MySingletonABC)

  assert instance1 is None

  MySingletonABC(1)

  instance2 = SingletonABCMeta.get_instance_or_none(MySingletonABC)

  assert instance2 is not None

  assert instance2.value == 1

def test_singleton_abc_instance_modification() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  instance1 = MySingletonABC(1)
  instance2 = MySingletonABC(2)

  instance1.value = 3
  assert instance2.value == instance1.value

  instance2.value = 4
  assert instance1.value == instance2.value

def test_singleton_abc_instance_deletion() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  instance1 = MySingletonABC(1)
  assert SingletonABCMeta.has_instance(MySingletonABC)

  SingletonABCMeta.detach(MySingletonABC)
  assert not SingletonABCMeta.has_instance(MySingletonABC)

  assert MySingletonABC not in SingletonABCMeta._refs #type: ignore
  assert MySingletonABC not in SingletonABCMeta._locks #type: ignore

  instance2 = MySingletonABC(2)
  assert instance1 is not instance2
  assert instance2.value == 2

def test_singleton_abc_instance_without_del() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  instance1 = NoDelSingletonABC(1)
  assert hasattr(instance1, "__del__")

  instance1.__del__() #type: ignore

  assert not SingletonABCMeta.has_instance(NoDelSingletonABC)

def test_singleton_abc_instance_with_existing_del() -> None:
  SingletonABCMeta.detach(MySingletonABC)

  instance1 = MySingletonABC(1)
  assert hasattr(instance1, "__del__")

  instance1.__del__()

  assert not SingletonABCMeta.has_instance(MySingletonABC)
