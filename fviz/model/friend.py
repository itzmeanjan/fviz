#!/usr/bin/python3

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Friend:
    '''
        Data class for holding information related to a facebook friend
        i.e. friend name and when these two became friend
    '''
    name: str
    _time: int

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self._time)


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
