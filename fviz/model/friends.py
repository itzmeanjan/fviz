#!/usr/bin/python3

from __future__ import annotations
from typing import List
from os.path import exists
from json import load
from .friend import Friend


class Friends:
    '''
        Data holder class for all friends,
        with their corresponding name
        and time when they became friend
    '''

    def __init__(self, friends: List[Friend]):
        self._friends = friends

    @property
    def friends(self) -> List[Friend]:
        return self._friends

    def getByIndex(self, idx: int) -> Friend:
        '''
            Returns friend by index of holding list
        '''
        if not (idx >= 0 and idx < len(self.friends)):
            return None

        return self.friends[idx]

    @staticmethod
    def fromJSON(src: str) -> Friends:
        '''
            Given path to JSON data file, returns 
            object holding all friends with their name
            and time when they became friend
        '''
        _obj = None
        try:

            if not exists(src):
                raise Exception('File doesn\'t exist !')

            _data = {}
            with open(src, mode='r') as fd:
                _data = load(fd)

            _obj = Friends(
                [Friend(i['name'], i['timestamp'])
                 for i in _data['friends']]
            )
        except Exception:
            _obj = None
        finally:
            return _obj


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
