from typing import Text
from .link import Link


class Replace(Link):
    """
    Replaces all occurrences of a specified substring with another substring.
    """

    def __init__(self, what: Text, to: Text):
        self.what = what
        self.to = to

    def process(self, text: Text):
        return text.replace(self.what, self.to)

    def __repr__(self):
        return (
            self._indentation + f'{type(self).__name__}("{self.what}" -> "{self.to}")'
        )
