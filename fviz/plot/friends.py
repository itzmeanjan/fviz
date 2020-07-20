#!/usr/bin/python3

from __future__ import annotations
from ..model.friends import Friends
from typing import Tuple, List
from datetime import timedelta


def _prepareDataForPlottingMonthlyFriendsCreated(friends: Friends) -> Tuple[List[str], List[int]]:
    '''
        Prepares data to be plotted along X & 
        Y axis for #-of friends created monthly
    '''
    if not friends:
        return None, None

    _start, _end = friends.getTimeFrame
    _x = []
    while _start <= _end:
        _x.append(_start.strftime('%b, %Y'))
        _start += timedelta(days=30)

    _x = list(set(_x))

    _buffer = friends.monthToFriendCount
    _y = [_buffer.get(i, 0) for i in _x]

    return _x, _y


def plotMonthlyFriendsCreated(friends: Friends, title: str, sink: str) -> bool:
    if not friends:
        return False

    try:
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
