from re import Pattern

from edri.utility.transformation import StringTransformer


class StringValidation(str):
    """
    A string type that performs validation on initialization.

    This class validates the string against optional constraints:
    - A regular expression pattern.
    - Minimum and maximum allowed lengths.

    Args:
        data (str): The input string to validate.
        maximum_length (int, optional): Maximum allowed length of the string.
        minimum_length (int, optional): Minimum required length of the string.
        regex (Pattern, optional): A compiled regex pattern the string must match.
        transformer (StringTransformer, optional): A StringTransformer instance to modify the string.
    Raises:
        ValueError: If the string does not match the regex,
                    or its length is outside the allowed bounds.

    Example:
        >>> StringValidation("hello", minimum_length=3, maximum_length=10)
        'hello'
    """

    def __new__(cls, data, /, *,
                maximum_length: int = None,
                minimum_length: int = None,
                regex: Pattern | None = None,
                transformer: StringTransformer | None = None,
                ):
        if regex is not None:
            if not regex.match(data):
                raise ValueError(f"Invalid data provided. Data '{data}' not match pattern '{regex.pattern}'")
        if minimum_length is not None and len(data) < minimum_length:
            raise ValueError(f"Invalid data provided. Data '{data}' is too short")
        if maximum_length is not None and len(data) > maximum_length:
            raise ValueError(f"Invalid data provided. Data '{data}' is too long")

        # Apply transformation (if provided)
        if transformer is not None:
            data = transformer.transform(data)

        return super().__new__(cls, data)


class IntegerValidation(int):
    """
    An integer type that performs validation on initialization.

    This class validates the integer against optional constraints:
    - Minimum and maximum allowed values.

    Args:
        data (int): The input integer to validate.
        minimum (int, optional): Minimum allowed value.
        maximum (int, optional): Maximum allowed value.

    Raises:
        ValueError: If the value is less than `minimum` or greater than `maximum`.

    Example:
        >>> IntegerValidation(5, minimum=1, maximum=10)
        5
    """

    def __new__(cls, data, /, *, minimum: int | None = None, maximum: int | None = None):
        if minimum is not None and data < minimum:
            raise ValueError(f"Invalid data provided. Data '{data}' is too small")
        if maximum is not None and data > maximum:
            raise ValueError(f"Invalid data provided. Data '{data}' is too big")
        return super().__new__(cls, data)


class FloatValidation(float):
    """
    A float type that performs validation on initialization.

    This class validates the float against optional constraints:
    - Minimum and maximum allowed values.

    Args:
        data (float): The input float to validate.
        minimum (float, optional): Minimum allowed value.
        maximum (float, optional): Maximum allowed value.

    Raises:
        ValueError: If the value is less than `minimum` or greater than `maximum`.

    Example:
        >>> FloatValidation(3.14, minimum=1.0, maximum=5.0)
        3.14
    """

    def __new__(cls, data, minimum: float | None = None, maximum: float | None = None):
        if minimum is not None and data < minimum:
            raise ValueError(f"Invalid data provided. Data '{data}' is too small")
        if maximum is not None and data > maximum:
            raise ValueError(f"Invalid data provided. Data '{data}' is too big")
        return super().__new__(cls, data)
