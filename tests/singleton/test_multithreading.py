from .config import MySingleton, MySingletonABC, n_threads
from threading import Thread

def test_singleton_multithreading() -> None:
  results: list[int] = []

  def create_instance(value: int) -> None:
    instance = MySingleton(value)
    results.append(instance.value)

  threads = [Thread(target=create_instance, args=(i,)) for i in range(n_threads)]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()

  result = results[0]
  assert all([value == result for value in results])

def test_singleton_abc_multithreading() -> None:
  results: list[int] = []

  def create_instance(value: int) -> None:
    instance = MySingletonABC(value)
    results.append(instance.value)

  threads = [Thread(target=create_instance, args=(i,)) for i in range(n_threads)]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()
    
  result = results[0]
  assert all([value == result for value in results])
