#!/usr/bin/python3

from typing import List
from os import walk
from os.path import join, abspath


def getMessageFilePaths(begin: str) -> List[str]:
    '''
        Returns all those file paths holding chats
    '''
    _buffer = []

    for root, _, files in walk(begin):
        if not files:
            continue

        for i in files:
            if i.startswith('message') and i.endswith('.json'):
                _buffer.append(abspath(join(root, i)))

    return _buffer


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
