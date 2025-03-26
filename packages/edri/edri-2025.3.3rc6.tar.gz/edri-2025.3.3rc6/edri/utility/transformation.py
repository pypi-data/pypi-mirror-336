from typing import Callable, Optional


class StringTransformer:
    """
    A class that allows transformation on initialization.
    The transformation can be predefined (like lowercasing) or custom using a lambda function.
    The transformation settings are stored and can be applied later via the `transform` method.

    Args:
        transform (callable, optional): A function that takes a string and returns a transformed version.
        lower (bool, optional): If True, the string will be converted to lowercase.
        upper (bool, optional): If True, the string will be converted to uppercase.

    Example:
        >>> st = StringTransformer("Hello", lower=True)
        >>> st.transform("Hello")
        'hello'

        >>> st = StringTransformer("Hello", transform=lambda x: x[::-1])
        >>> st.transform("Hello")
        'olleH'
    """

    def __init__(self, *,
                 transform: Optional[Callable[[str], str]] = None,
                 lower: bool = False,
                 upper: bool = False):

        # Store the transformation settings
        self._transform: Optional[Callable[[str], str]] = transform
        self._lower: bool = lower
        self._upper: bool = upper

    def transform(self, value: str) -> str:
        """
        Apply the stored transformations to the given value.

        Args:
            value (str): The string to be transformed.

        Returns:
            str: The transformed string.
        """
        # Predefined transformations (lower/upper)
        if self._lower:
            value = value.lower()
        if self._upper:
            value = value.upper()

        # Apply the custom transformation function if provided
        if self._transform is not None:
            value = self._transform(value)

        return value
