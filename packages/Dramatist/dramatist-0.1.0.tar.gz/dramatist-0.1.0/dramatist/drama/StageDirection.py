from typing import List
from dramatist.drama.ScenePart import ScenePart


class StageDirection(ScenePart):
    _text: str = ''

    def __init__(self, text: str):
        self.tokens: List[str] = list()
        self.token_count = 0
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, v: str):
        self._text = v
        self.tokens = v.split(' ')
        self.token_count = len(self.tokens)
