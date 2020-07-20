#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime


class Friend:
    '''
        Data class for holding information related to a facebook friend
        i.e. friend name and when these two became friend
    '''

    def __init__(self, name: str, time: int):
        self._name = name
        self._time = time

    @property
    def name(self) -> str:
        return self._name

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self._time)


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
