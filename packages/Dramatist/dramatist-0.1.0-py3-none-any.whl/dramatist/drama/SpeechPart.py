from typing import List
from dramatist.drama.Markup import Markup


class SpeechPart:
    TYPE_SPEECH_LINE = 0
    TYPE_SPEECH_P_B = 1
    TYPE_SPEECH_P = 2
    TYPE_STAGE_DIRECTION = 3
    TYPE_STAGE_DIRECTION_INLINE = 4
    # For counting, we run into issues, when a p-block starts with a stage direction. So we need a special type
    # TODO: Could this be improved?
    TYPE_STAGE_DIRECTION_COUNT = 5

    _text: str = ''

    def __init__(self, text: str, speech_type: int, markups: List[Markup]):
        self.type = speech_type
        self.tokens: List[str] = list()
        self.token_count = 0
        self.char_count = 0
        self.text = text
        self.markups = markups

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, v: str):
        self._text = v
        self.tokens = v.split(' ')
        self.token_count = len(self.tokens)
        self.char_count = len(v)
