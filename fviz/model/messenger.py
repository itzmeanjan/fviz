#!/usr/bin/python3

from __future__ import annotations
from .messages import Messages
from typing import List


class Messenger:
    def __init__(self, inbox: List[Messages]):
        self._inbox = inbox

    @property
    def inbox(self) -> List[Messages]:
        return self._inbox

    @property
    def count(self) -> int:
        return len(self._inbox)

    def byIndex(self, _idx: int) -> Messages:
        return self._inbox[_idx] if _idx >= 0 and _idx < self.count else None


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
