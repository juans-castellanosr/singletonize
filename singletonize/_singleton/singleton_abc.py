"""Abstract Base Singleton implementation."""
from .._metaclasses import SingletonABCMeta
from ._base_singleton import BaseSingleton

class SingletonABC(BaseSingleton, metaclass=SingletonABCMeta):
  """
  Abstract Base Singleton Class
  ==============================

  This module provides an abstract base class (ABC) implementation of the Singleton pattern,
  ensuring that subclasses adhere to the singleton behavior while allowing for abstract methods.

  <br>

  ## Overview
  The `SingletonABC` class should be inherited by any abstract class that needs to be a Singleton.
  It uses `SingletonABCMeta` as its metaclass, ensuring that only one instance of any concrete subclass exists.

  <br>

  ## Example Usage
  ```python
  from abc import abstractmethod

  class AbstractExample(SingletonABC):
    @abstractmethod
    def some_method(self):
      pass

  class ConcreteExample(AbstractExample):
    def __init__(self, value: int):
      self.a = value

    def some_method(self):
      return self.a

  # Creating a singleton instance
  singleton_instance = ConcreteExample.get_instance(10)
  assert singleton_instance.some_method() == 10
  ```

  ## Methods

  ### `get_instance(*args, **kwargs) -> Instance`
  Returns the existing singleton instance or creates a new one if it doesn't exist.

  #### Example:
  ```python
  instance = ConcreteExample.get_instance(1)
  ```

  <br>

  ### `has_instance() -> bool`
  Checks if a singleton instance exists.

  #### Example:
  ```python
  exists = ConcreteExample.has_instance()
  ```

  <br>

  ### `detach() -> None`
  Removes the existing singleton instance. Can be called from the class or instance.

  #### Example:
  ```python
  ConcreteExample.detach()
  # or
  instance.detach()
  ```

  <br>

  ### `reset_instance(*args, **kwargs) -> Instance`
  Replaces the existing singleton instance with a new one, using the provided arguments.

  #### Example:
  ```python
  ConcreteExample.reset_instance(2)
  # or
  instance.reset_instance(2)
  ```

  <br>

  ### `get_instance_or_none() -> Instance | None`
  Returns the singleton instance if it exists, otherwise returns `None`.

  #### Example:
  ```python
  instance = ConcreteExample.get_instance_or_none()
  ```

  <br>

  ### `is_instance(obj) -> bool`
  Checks if the given object is the singleton instance.

  #### Example:
  ```python
  is_instance = ConcreteExample.is_instance(instance)
  ```

  <br>

  ### `update_instance(**kwargs) -> None`
  Updates the singleton instance's attributes with new values.

  #### Example:
  ```python
  ConcreteExample.update_instance(a=2)
  # or
  instance.update_instance(a=2)
  ```

  <br>

  ### `instance_as_dict() -> dict`
  Returns the singleton instance's attributes as a dictionary.

  #### Example:
  ```python
  instance_dict = ConcreteExample.instance_as_dict()
  # or
  instance_dict = instance.instance_as_dict()
  ```
  """

  __slots__ = ()
