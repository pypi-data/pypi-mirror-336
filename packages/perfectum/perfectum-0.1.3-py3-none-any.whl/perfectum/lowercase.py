from typing import Text
from .link import Link


class Lowercase(Link):
    """
    Converts text to lowercase.
    """

    def process(self, text: Text):
        return text.lower()
