from typing import Text
import unicodedata
from .normalize_unicode import NormalizeUnicode


class Asciify(NormalizeUnicode):
    """
    Converts Unicode text to ASCII by removing diacritics and non-ASCII characters.
    """

    def __init__(self, level=0):
        super().__init__("NFKD", level)

    def process(self, text: Text):
        text = super().process(text)
        return "".join(
            [character for character in text if not unicodedata.combining(character)]
        )

    def __repr__(self):
        return self._indentation + type(self).__name__
