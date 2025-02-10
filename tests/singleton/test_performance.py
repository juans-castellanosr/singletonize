from .config import MySingleton, MySingletonABC, n_threads
import pytest
from concurrent.futures import ThreadPoolExecutor
from typing import Any

@pytest.mark.benchmark(group="singleton")
def test_singleton_performance(benchmark: Any) -> None:
  def create_instance() -> MySingleton:
    return MySingleton(1)
  
  benchmark(create_instance)

@pytest.mark.benchmark(group="singleton_abc")
def test_singleton_abc_performance(benchmark: Any) -> None:
  def create_instance() -> MySingletonABC:
    return MySingletonABC(1)
    
  benchmark(create_instance)

@pytest.mark.benchmark(group="singleton_multithreading")
def test_singleton_multithreading_performance(benchmark: Any) -> None:
  results: list[int] = []

  def create_instance(value: int) -> None:
    instance = MySingleton(value)
    results.append(instance.value)
      
  def run_multithreaded() -> None:
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
      executor.map(create_instance, range(n_threads))

  benchmark(run_multithreaded)

  result = results[0]
  assert all(value == result for value in results)
  
@pytest.mark.benchmark(group="singleton_abc_multithreading")
def test_singleton_abc_multithreading_performance(benchmark: Any) -> None:
  results: list[int] = []

  def create_instance(value: int) -> None:
    instance = MySingletonABC(value)
    results.append(instance.value)
      
  def run_multithreaded() -> None:
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
      executor.map(create_instance, range(n_threads))

  benchmark(run_multithreaded)

  result = results[0]
  assert all(value == result for value in results)