#!/usr/bin/python3

from __future__ import annotations
from .messages import Messages
from typing import List, Dict, Any
from json import load
from functools import reduce


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

    @staticmethod
    def fromJSON(src: List[str]) -> Messenger:
        '''
           Reads each JSON file content, holding messages
           and objectifies them, finally forming Messenger object,
           which can be manipulated later
        '''

        def _getFileContent(path: str) -> Dict[str, Any]:
            _content = None
            with open(path, mode='r') as fd:
                _content = load(fd)
            return _content

        return Messenger(
            list(
                filter(lambda e: e,
                       reduce(
                           lambda acc, cur: acc +
                           [Messages.fromJSON(_getFileContent(cur))],
                           src,
                           []))))


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
