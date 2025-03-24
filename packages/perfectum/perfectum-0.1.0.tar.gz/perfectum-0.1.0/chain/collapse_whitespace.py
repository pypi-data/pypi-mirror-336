from .pattern_replace import PatternReplace


class CollapseWhitespace(PatternReplace):
    """
    Collapses multiple consecutive spaces into a single space.
    """

    def __init__(self):
        super().__init__(" {2,}", " ")

    def __repr__(self):
        return self._indentation + type(self).__name__
