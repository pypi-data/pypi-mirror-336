from typing import Text
from .link import Link

try:
    import g4f

    g4f.debug.logging = False
    g4f.debug.version_check = False
except ImportError:
    g4f = None


class Gpt(Link):
    """
    Processes text using AI.
    """

    def __init__(self, model: Text, prompt: Text, level=0):
        super().__init__(level)
        self.model = model
        self.prompt = prompt

    def process(self, text: Text):
        if g4f is None:
            raise RuntimeError('requires "gpt" feature enabled.')

        return g4f.ChatCompletion.create(
            self.model,
            [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": text},
            ],
        )

    def __repr__(self):
        return (
            self._indentation
            + f'{type(self).__name__}("{self.model}", "{self.prompt}")'
        )
