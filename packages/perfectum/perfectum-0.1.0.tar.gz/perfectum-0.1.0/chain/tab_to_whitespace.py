from .replace import Replace

DEFAULT_LENGTH = 4


class TabToWhitespace(Replace):
    """
    Replaces tab characters with equivalent whitespace spaces.
    """

    def __init__(self, length=DEFAULT_LENGTH):
        self.length = length
        super().__init__("\t", " " * self.length)

    def __repr__(self):
        return self._indentation + f"{type(self).__name__}({self.length})"
