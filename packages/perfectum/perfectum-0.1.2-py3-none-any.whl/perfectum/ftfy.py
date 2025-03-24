from typing import Text
from .link import Link

try:
    import ftfy
except ImportError:
    ...


class Ftfy(Link):
    """
    Fixes text encoding issues and mojibake using ftfy library corrections.
    """

    def process(self, text: Text):
        return ftfy.fix_text(text, normalization=None)
