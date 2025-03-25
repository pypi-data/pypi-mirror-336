from typing import Text
from .link import Link
import asyncio

try:
    import googletrans
except ImportError:
    googletrans = None


class Translate(Link):
    """
    Translates text to a specified language using the Google translation service.
    """

    def __init__(self, language: Text, level=0):
        super().__init__(level)
        self.language = language

        if googletrans is None:
            raise RuntimeError('requires "translate" feature enabled.')

        self.service = googletrans.Translator()

    def process(self, text: Text):
        async def translate():
            return await self.service.translate(text, dest=self.language)

        return asyncio.run(translate()).text

    def __repr__(self):
        return self._indentation + f'{type(self).__name__}("{self.language}")'
