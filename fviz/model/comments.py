#!/usr/bin/python3

from __future__ import annotations
from typing import List
from os.path import exists
from json import load
from .comment import Comment


class Comments:
    def __init__(self, comments: List[Comment]):
        self._comments = comments

    @property
    def comments(self) -> List[Comment]:
        '''
            List of all comments
        '''
        return self._comments

    @property
    def count(self) -> int:
        '''
            Count of all comments
        '''
        return len(self._comments)

    def byIndex(self, _idx: int) -> Comment:
        '''
            Retrieves comment by its index
        '''
        return self._comments[_idx]\
            if _idx >= 0 and _idx < self.count\
            else None

    @staticmethod
    def fromJSON(src: str) -> Comments:
        '''
            Given a JSON data file, holding all comments by this
            facebook user, we'll form a Comments obj, for performing several interesting ops
            on it
        '''
        if not exists(src):
            return None

        _buffer = []

        with open(src, mode='r') as fd:
            _buffer = load(fd)
        if 'comments' not in _buffer:
            return None

        _comments = Comments([])

        for i in _buffer['comments']:
            _comments._comments.append(
                Comment(i['title'],
                        i['timestamp'],
                        i.get('data', [])))

        return _comments


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
