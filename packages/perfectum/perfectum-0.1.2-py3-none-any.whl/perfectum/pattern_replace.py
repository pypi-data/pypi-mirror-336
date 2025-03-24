from typing import Text
from .link import Link
import re


class PatternReplace(Link):
    """
    Replaces text matching a regex pattern with specified replacement.
    """

    def __init__(self, pattern: Text, to: Text):
        self.raw_pattern = pattern
        self.pattern = re.compile(pattern)
        self.to = to

    def process(self, text: Text):
        return self.pattern.sub(self.to, text)

    def __repr__(self):
        return (
            self._indentation
            + f'{type(self).__name__}("{self.raw_pattern}" -> "{self.to}")'
        )
