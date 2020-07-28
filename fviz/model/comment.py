#!/usr/bin/python3

from typing import List, Dict, Any
from datetime import datetime
from re import compile as regCompile, I as regI, Match


class Comment:
    def __init__(self, title: str, timestamp: int, data: List[Dict[str, Dict[str, Any]]]):
        self._title = title
        self._time = timestamp
        if data:
            self._data = data

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self._time)

    @property
    def title(self) -> str:
        return self._title

    @property
    def _getRegex(self) -> Match:
        regex = regCompile(
            r'((commented\son|replied\sto)\s(.+)\s(.+)\.)',
            flags=regI)

        return regex.search(self._title)

    @property
    def peer(self) -> str:
        _match = self._getRegex

        if not _match:
            return None
        return _match.group(3)[:-2]\
            if _match.group(3).endswith('\'s') else\
            (None if _match.group(3) == 'a'
             else 'self')

    @property
    def contentType(self) -> str:
        _match = self._getRegex

        if not _match:
            return None
        return _match.group(4)

    @property
    def isConversation(self) -> bool:
        _match = self._getRegex

        if not _match:
            return False

        return _match.group(2) == 'replied to' and _match.group(4) == 'comment'


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
