from typing import Sequence, Text
from .link import Link


class Chain(Link):
    """
    Executes text processing through a sequence of chained transformation steps.
    """

    def __init__(self, chain: Sequence[Link], level=0):
        super().__init__(level)
        self.chain = []
        for link in chain:
            link._level(level + 1)
            self.chain.append(link)

    def process(self, text: Text):
        for link in self.chain:
            text = link.process(text)
        return text

    def __repr__(self):
        output = self._indentation + "Chain ["
        for link in self.chain:
            output += "\n" + self._indentation + str(link) + ","
        output += "\n" + self._indentation + "]"
        return output
