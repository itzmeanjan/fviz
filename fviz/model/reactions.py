#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from datetime import datetime
from os.path import exists
from json import load
from .reactedContent import ReactedContent


class Reactions:
    '''
        Holds all reacted content realated information made by an actor
        in form of an ordered listed ( chronologically decreasing )
    '''

    def __init__(self, reactions: List[ReactedContent]):
        self._reactions = reactions

    @property
    def count(self) -> int:
        '''
            Number of all reactions by actor
        '''
        return len(self._reactions)

    @property
    def getTimeFrame(self) -> Tuple[datetime, datetime]:
        '''
            Timeframe of all reactions present in data set, i.e.
            returns a 2-element tuple of datetimes, where first one
            is starting point & another one is ending point
        '''
        return self._reactions[self.count - 1].time, self._reactions[0].time

    @staticmethod
    def fromJSON(src: str) -> Reactions:
        '''
            Given path to data file, returns instance of this class
            holding all reacted contents, by actor
        '''
        if not exists(src):
            return None
        try:
            data = None
            with open(src, 'r') as fd:
                data = load(fd)

            if not data:
                return None

            return Reactions(
                list(map(lambda e: ReactedContent(e.get('title'),
                                                  e.get('data')[0].get(
                    'reaction').get('reaction'),
                    e.get('data')[0].get(
                    'reaction').get('actor'),
                    e.get('timestamp')), data['reactions']))
            )
        except Exception:
            return None


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
