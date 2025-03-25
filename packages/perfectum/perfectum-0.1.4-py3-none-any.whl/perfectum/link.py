from typing import Text


class Link:
    """
    Base class for creating text processing steps in a transformation chain.
    """

    def __init__(self, level=0):
        self._level(level)

    def _level(self, level):
        self._indentation = " " * 4 * level

    def process(self, text: Text):
        raise NotImplementedError('implement your text-processing logic in the "process" function')

    def __repr__(self):
        return self._indentation + type(self).__name__
