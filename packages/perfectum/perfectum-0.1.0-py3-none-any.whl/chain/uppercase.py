from typing import Text
from .link import Link


class Uppercase(Link):
    """
    Converts text to uppercase.
    """

    def process(self, text: Text):
        return text.upper()
