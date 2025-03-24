from typing import Text
from .link import Link
import asyncio

try:
    from googletrans import Translator
except ImportError:
    ...


class Translate(Link):
    """
    Translates text to a specified language using the Google translation service.
    """

    def __init__(self, language: Text, level=0):
        super().__init__(level)
        self.language = language
        self.service = Translator()

    def process(self, text: Text):
        async def translate():
            return await self.service.translate(text, dest=self.language)

        return asyncio.run(translate())

    def __repr__(self):
        return self._indentation + f'{type(self).__name__}("{self.language}")'
