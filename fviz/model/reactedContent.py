#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime


class ReactedContent:
    '''
        Holds information related to reaction,
        given by actor to some content on facebook
    '''

    def __init__(self, title: str, reaction: str, actor: str, timestamp: int):
        self._title = title
        self._reaction = reaction
        self._actor = actor
        self._timestamp = timestamp

    @property
    def title(self) -> str:
        return self._title

    @property
    def reaction(self) -> str:
        return self._reaction

    @property
    def actor(self) -> str:
        return self._actor

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
