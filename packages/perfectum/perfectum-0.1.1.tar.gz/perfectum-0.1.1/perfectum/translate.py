from typing import Text
from .link import Link

try:
    from translate import Translator
except ImportError:
    ...


class Translate(Link):
    """
    Translates text to a specified language using the Google translation service.
    """

    def __init__(self, language: Text, level=0):
        super().__init__(level)
        self.language = language
        self.service = Translator(to_lang=language)

    def process(self, text: Text):
        return self.service.translate(text)

    def __repr__(self):
        return self._indentation + f'{type(self).__name__}("{self.language}")'
