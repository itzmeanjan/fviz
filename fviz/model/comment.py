#!/usr/bin/python3

from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime
from re import compile as regCompile, I as regI


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
    def peer(self) -> str:
        regex = regCompile(
            r'((commented\son|replied\sto)\s(.+)\s(.+)\.)',
            flags=regI)

        _match = regex.search(self._title)

        if not _match:
            return None
        else:
            return _match.group(3)[:-2]\
                if _match.group(3).endswith('\'s')\
                else _match.group(3)

    @property
    def contentType(self) -> str:
        regex = regCompile(
            r'((commented\son|replied\sto)\s(.+)\s(.+)\.)',
            flags=regI)

        _match = regex.search(self._title)

        if not _match:
            return None
        else:
            return _match.group(4)


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
