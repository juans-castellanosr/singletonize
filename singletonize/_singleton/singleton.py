"""Concrete Singleton implementation."""
from ._base_singleton import BaseSingleton
from .._metaclasses import SingletonMeta

class Singleton(BaseSingleton, metaclass=SingletonMeta):
  """
  Singleton Class Implementation
  ================================

  This module provides a flexible Singleton implementation using metaclasses,
  ensuring that only one instance of a class is created and maintained.

  <br>

  ## Overview
  The `Singleton` class should be inherited by any class that needs a Singleton behavior.
  It uses `SingletonMeta` as its metaclass, which ensures that a single instance exists.

  <br>

  ## Example Usage
  ```python
  class Test(Singleton):
    def __init__(self, value: int):
      self.a = value

  # Creating a singleton instance
  singleton_instance = Test(10)
  # or
  # singleton_instance = Test.get_instance(10)

  # Retrieving the same instance
  same_instance = Test()
  # or
  # same_instance = Test.get_instance()
  assert singleton_instance is same_instance  # True
  ```

  <br>

  ## Methods

  ### `get_instance(*args, **kwargs) -> Instance`
  Returns the existing singleton instance or creates a new one if it doesn't exist.

  #### Example:
  ```python
  test = Test.get_instance(1)
  ```

  <br>

  ### `has_instance() -> bool`
  Checks if a singleton instance exists.

  #### Example:
  ```python
  exists = Test.has_instance()
  ```

  <br>

  ### `detach() -> None`
  Removes the existing singleton instance. Can be called from the class or instance.

  #### Example:
  ```python
  Test.detach()
  # or
  test.detach()
  ```

  <br>

  ### `reset_instance(*args, **kwargs) -> Instance`
  Replaces the existing singleton instance with a new one, using the provided arguments.

  #### Example:
  ```python
  Test.reset_instance(2)
  # or
  test.reset_instance(2)
  ```

  <br>

  ### `get_instance_or_none() -> Instance | None`
  Returns the singleton instance if it exists, otherwise returns `None`.

  #### Example:
  ```python
  test = Test.get_instance_or_none()
  ```

  <br>

  ### `is_instance(obj) -> bool`
  Checks if the given object is the singleton instance.

  #### Example:
  ```python
  is_instance = Test.is_instance(test)
  ```

  <br>

  ### `update_instance(**kwargs) -> None`
  Updates the singleton instance's attributes with new values.

  #### Example:
  ```python
  Test.update_instance(a=2)
  # or
  test.update_instance(a=2)
  ```

  <br>

  ### `instance_as_dict() -> dict`
  Returns the singleton instance's attributes as a dictionary.

  #### Example:
  ```python
  instance_dict = Test.instance_as_dict()
  # or
  instance_dict = test.instance_as_dict()
  ```
  """

  __slots__ = ()
