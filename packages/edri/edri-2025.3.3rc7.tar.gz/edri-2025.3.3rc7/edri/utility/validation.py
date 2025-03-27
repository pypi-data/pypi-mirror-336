from re import Pattern


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
    Raises:
        ValueError: If the string does not match the regex,
                    or its length is outside the allowed bounds.

    Example:
        >>> StringValidation("hello", minimum_length=3, maximum_length=10)
        'hello'
    """

    def __new__(cls, value, /, *,
                maximum_length: int = None,
                minimum_length: int = None,
                regex: Pattern | None = None,
                ):

        value = super().__new__(cls, value)
        if regex is not None:
            if not regex.match(value):
                raise ValueError(f"Invalid data provided. Data '{value}' not match pattern '{regex.pattern}'")
        if minimum_length is not None and len(value) < minimum_length:
            raise ValueError(f"Invalid data provided. Data '{value}' is too short")
        if maximum_length is not None and len(value) > maximum_length:
            raise ValueError(f"Invalid data provided. Data '{value}' is too long")

        return value


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

    def __new__(cls, value, /, *, minimum: int | None = None, maximum: int | None = None):
        value = super().__new__(cls, value)
        if minimum is not None and value < minimum:
            raise ValueError(f"Invalid data provided. Data '{value}' is too small")
        if maximum is not None and value > maximum:
            raise ValueError(f"Invalid data provided. Data '{value}' is too big")
        return value


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

    def __new__(cls, value, minimum: float | None = None, maximum: float | None = None):
        value = super().__new__(cls, value)
        if minimum is not None and value < minimum:
            raise ValueError(f"Invalid data provided. Data '{value}' is too small")
        if maximum is not None and value > maximum:
            raise ValueError(f"Invalid data provided. Data '{value}' is too big")
        return value
