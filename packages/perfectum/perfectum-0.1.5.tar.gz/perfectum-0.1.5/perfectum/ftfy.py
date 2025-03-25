from typing import Text
from .link import Link

try:
    import ftfy
except ImportError:
    ftfy = None


class Ftfy(Link):
    """
    Fixes text encoding issues and mojibake using ftfy library corrections.
    """

    def process(self, text: Text):
        if ftfy is None:
            raise RuntimeError('requires "ftfy" feature enabled.')

        return ftfy.fix_text(text, normalization=None)
