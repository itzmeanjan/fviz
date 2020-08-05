#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict
from os.path import exists
from json import load
from .comment import Comment
from collections import Counter
from datetime import time


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

    def topXPeersWithMostInvolvementInComments(self, x: int = 10) -> List[Tuple[str, int]]:
        '''
            Finds top X number of peers, their posts
            were where this user mostly commented

            Note: This function doesn't consider those
            comments where it's a reply to another comment i.e.
            part of a comment based conversation
        '''
        buffer = {}

        for i in self.comments:
            _peer = i.peer
            if _peer:
                buffer[_peer] = buffer.get(_peer, 0) + 1

        return Counter(buffer).most_common(x)

    @property
    def peerToCommentCount(self) -> Dict[str, int]:
        '''
            Keeps count for which peer ( facebook profile ) is 
            associated with how many comments.
        '''
        _buffer = {}

        for i in self.comments:
            _peer = i.peer
            if not _peer:
                continue

            _buffer[_peer] = _buffer.get(_peer, 0) + 1

        return _buffer

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

    @property
    def groupByWeek(self) -> Dict[str, List[int]]:
        '''
            Groups all comments you made by its
            week of happening where week is specified as
            `Week %W, %Y`
        '''
        buffer = {}

        for i, j in enumerate(self.comments):
            _dt = j.time.date()
            _week = 'Week {}, {}'.format(
                int(_dt.strftime('%W'), base=10) + 1,
                _dt.strftime('%Y'))

            if _week not in buffer:
                buffer[_week] = [i]
            else:
                buffer[_week].append(i)

        return buffer

    @property
    def weekToQuarterOfDayAndCount(self) -> Dict[str, Dict[str, int]]:
        '''
            Mapping all comemnts ( you made on facebook ) into their corresponding week of 
            happening where each of them ( week identifier ) will hold record of which quarter
            of a day is having how many likes and reactions count for that span
            of week

            Gives an idea about how you spent your week on facebook ( commenting on posts/ photos/ videos etc )
            on which quarter you were mostly active/ inactive and how did that change over time.
        '''
        def mapIntoQuarters(_data: List[int]) -> Dict[str, int]:
            _mappedIntoQuarters = {}

            _06hr = time(6, 0, 0)
            _12hr = time(12, 0, 0)
            _18hr = time(18, 0, 0)

            for i in _data:
                _tm = self.byIndex(i).time.time()

                if _tm < _06hr:
                    _mappedIntoQuarters['00:00 - 05:59'] =\
                        _mappedIntoQuarters.get('00:00 - 06:00',
                                                0) + 1
                elif _tm >= _06hr and _tm < _12hr:
                    _mappedIntoQuarters['06:00 - 11:59'] =\
                        _mappedIntoQuarters.get('06:00 - 11:59',
                                                0) + 1
                elif _tm >= _12hr and _tm < _18hr:
                    _mappedIntoQuarters['12:00 - 17:59'] =\
                        _mappedIntoQuarters.get('12:00 - 17:59',
                                                0) + 1
                else:
                    _mappedIntoQuarters['18:00 - 23:59'] =\
                        _mappedIntoQuarters.get('18:00 - 23:59',
                                                0) + 1

            return _mappedIntoQuarters

        return dict([(k, mapIntoQuarters(v)) for k, v in self.groupByWeek.items()])


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
