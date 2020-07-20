#!/usr/bin/python3

from __future__ import annotations
from typing import List
from os.path import exists
from json import load
from .friend import Friend


class Friends:
    def __init__(self, friends: List[Friend]):
        self._friends = friends

    @property
    def friends(self) -> List[Friend]:
        return self._friends

    @staticmethod
    def fromJSON(src: str) -> Friends:
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
