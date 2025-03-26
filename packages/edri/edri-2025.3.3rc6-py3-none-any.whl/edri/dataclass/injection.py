from dataclasses import dataclass
from typing import Any


@dataclass
class Injection[T]:
    """
    Represents a declarative injection of a class along with its initialization parameters.

    This is typically used in a dependency injection context where you want to defer
    instantiation and instead describe how something should be constructed.

    Attributes:
        cls (T): The class type to be injected.
        parameters (dict[str, Any]): Keyword arguments to pass to the class constructor.

    Example:
        Injection(MyService, parameters={'config': config, 'db': db})
    """
    cls: T
    parameters: dict[str, Any]
