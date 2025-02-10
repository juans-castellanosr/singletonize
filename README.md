# Singletonize for Python

[![PyPI version](https://badge.fury.io/py/singletonize.svg)](https://pypi.org/project/singletonize/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Publish to PyPi](https://github.com/juans-castellanosr/singletonize/actions/workflows/publish.yml/badge.svg)](https://github.com/juans-castellanosr/singletonize/actions/workflows/publish.yml)

## Overview

**Singletonize** is a Python package providing a robust, thread-safe Singleton pattern implementation using metaclasses. It ensures strict singleton enforcement while offering useful utilities for instance management.

## Features

- **Strict Singleton Enforcement**: Ensures only one instance of a class exists.
- **Abstract Base Singleton Support**: Allows defining abstract singleton classes.
- **Thread-Safe Implementation**: Uses metaclasses for thread safety.
- **Instance Management Utilities**: Methods for checking, resetting, updating, and serializing instances.
- **Fully Typed with MyPy**: Ensures type safety.
- **Modern Package Management with Poetry**: Streamlined dependency and package management.

## Installation

Install using `pip`:

```sh
pip install singletonize
```

Or with `poetry`:

```sh
poetry add singletonize
```

## Usage

### Basic Singleton Example

```python
from singletonize import Singleton

class ExampleSingleton(Singleton):
    def __init__(self, value: int):
        self.value = value

# Creating an instance
instance1 = ExampleSingleton(10)
instance2 = ExampleSingleton.get_instance()

assert instance1 is instance2  # True
assert instance1.value == instance2.value == 10  # True
```

### Abstract Base Singleton

```python
from singletonize import SingletonABC
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
singleton_instance = ConcreteExample(10)
assert singleton_instance.some_method() == 10
```

### Instance Management

```python
# Checking if an instance exists
assert ExampleSingleton.has_instance()  # True

# Getting the instance or None
instance = ExampleSingleton.get_instance_or_none()

# Updating instance attributes
ExampleSingleton.update_instance(value=20)
assert instance.value == 20

# Converting instance to dictionary
instance_dict = ExampleSingleton.instance_as_dict()
print(instance_dict)  # {'value': 20}

# Resetting the instance
ExampleSingleton.reset_instance(30)
assert ExampleSingleton.get_instance().value == 30
```

## Performance Benchmark

Singletonize has been benchmarked to evaluate its efficiency in both single-threaded and multi-threaded environments.

### Single-threaded Performance

#### Standard Singleton

| Name                       | Min (ns) | Max (ns)    | Mean (ns) | StdDev (ns) | Median (ns) | IQR (ns) | Outliers  | OPS (Mops/s) | Rounds | Iterations |
| -------------------------- | -------- | ----------- | --------- | ----------- | ----------- | -------- | --------- | ------------ | ------ | ---------- |
| test_singleton_performance | 493.0189 | 29,423.0122 | 566.5408  | 424.3932    | 535.0157    | 20.0234  | 2081;8156 | 1.7651       | 114969 | 1          |

#### SingletonABC

| Name                           | Min (ns) | Max (ns)   | Mean (ns) | StdDev (ns) | Median (ns) | IQR (ns) | Outliers   | OPS (Mops/s) | Rounds | Iterations |
| ------------------------------ | -------- | ---------- | --------- | ----------- | ----------- | -------- | ---------- | ------------ | ------ | ---------- |
| test_singleton_abc_performance | 418.9002 | 7,668.2001 | 461.9932  | 96.6991     | 445.9507    | 8.2495   | 3741;12382 | 2.1645       | 108425 | 20         |

### Multi-threaded Performance

#### SingletonABC with Multithreading

| Name                                          | Min (ms) | Max (ms) | Mean (ms) | StdDev (ms) | Median (ms) | IQR (ms) | Outliers | OPS     | Rounds | Iterations |
| --------------------------------------------- | -------- | -------- | --------- | ----------- | ----------- | -------- | -------- | ------- | ------ | ---------- |
| test_singleton_abc_multithreading_performance | 11.7924  | 25.3676  | 13.9574   | 3.3869      | 12.5568     | 1.0450   | 11;11    | 71.6466 | 70     | 1          |

#### Standard Singleton with Multithreading

| Name                                      | Min (ms) | Max (ms) | Mean (ms) | StdDev (ms) | Median (ms) | IQR (ms) | Outliers | OPS     | Rounds | Iterations |
| ----------------------------------------- | -------- | -------- | --------- | ----------- | ----------- | -------- | -------- | ------- | ------ | ---------- |
| test_singleton_multithreading_performance | 11.8365  | 22.9825  | 13.9596   | 3.3061      | 12.7048     | 1.2596   | 8;8      | 71.6355 | 53     | 1          |

These benchmarks indicate that `SingletonABC` has slightly better performance in single-threaded scenarios, while both implementations perform similarly under multi-threaded conditions.

## Development

### Setting Up the Project

1. Clone the repository:

   ```sh
   git clone https://github.com/juans-castellanosr/singletonize.git
   cd singletonize
   ```

2. Install dependencies using `poetry`:

   ```sh
   poetry install
   ```

### Code Quality & Type Checking

This project enforces strict type checking and linting:

```sh
mypy singletonize
ruff check singletonize
```

### Running Tests

Tests are managed with `pytest`:

```sh
pytest tests/
```

Performance benchmarks can be run using:

```sh
pytest --benchmark-only
```

## Contributing

We welcome contributions! Follow these guidelines to ensure smooth collaboration:

### Forking and Branching Strategy

1. **Fork** the repository and clone it locally.
2. **Create a branch** from `development`:
   ```sh
   git checkout -b feature/your-feature development
   ```
3. **Make your changes** and commit with meaningful messages.
4. **Push your branch** to your fork:
   ```sh
   git push origin feature/your-feature
   ```
5. **Create a Pull Request (PR) to the `development` branch**.
6. **Wait for approval** and feedback before merging.

### Code Standards

- Follow PEP8 (`ruff` is used for linting).
- Use `mypy` for type checking.
- Ensure all tests pass before submitting PRs.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

For support, open an issue or contact the maintainers via GitHub Discussions.

---

Happy coding! 🚀
