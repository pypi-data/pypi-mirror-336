from typing import Text
from .link import Link


class Trim(Link):
    """
    Removes leading and trailing whitespace from text.
    """

    def process(self, text: Text):
        return text.strip()
