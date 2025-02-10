__all__ = ['MySingleton', 'MySingletonABC', 'n_threads']

from singletonize import Singleton, SingletonABC

n_threads = 1000

class MySingleton(Singleton):
  def __init__(self, value: int) -> None:
    self.value = value

class MySingletonABC(SingletonABC):
  def __init__(self, value: int):
    self.value = value
