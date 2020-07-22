#!/usr/bin/python3

from __future__ import annotations
from typing import List
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


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
