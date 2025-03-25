from typing import Text
import unicodedata
from .link import Link

DEFAULT_FORM = "NFD"


class NormalizeUnicode(Link):
    """
    Normalizes Unicode text to a specified form.
    """

    def __init__(self, form=DEFAULT_FORM, level=0):
        super().__init__(level)
        self.form = form

    def process(self, text: Text):
        return unicodedata.normalize(self.form, text)

    def __repr__(self):
        return self._indentation + f'{type(self).__name__}("{self.form}")'
