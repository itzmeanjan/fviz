#!/usr/bin/python3

from __future__ import annotations
from typing import List
from .comment import Comment


class Comments:
    def __init__(self, comments: List[Comment]):
        self._comments = comments

    @property
    def comments(self) -> List[Comment]:
        return self._comments


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
