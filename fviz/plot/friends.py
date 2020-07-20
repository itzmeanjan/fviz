#!/usr/bin/python3

from __future__ import annotations
from ..model.friends import Friends
from typing import Tuple, List
from datetime import timedelta
import seaborn as sns
from matplotlib import pyplot as plt
from math import ceil


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

        _x, _y = _prepareDataForPlottingMonthlyFriendsCreated(friends)

        sns.set(style='darkgrid')

        _fig, _axes = plt.subplots(
            ceil(len(_x)/12), 1, figsize=(16, ceil(len(_x)/12) * 8), dpi=100)

        _start = 0
        _end = 12

        for i in _axes:
            _tmpX = _x[_start: _end]

            sns.lineplot(
                x=_tmpX,
                y=_y[_start: _end],
                ax=i
            )

            i.set_xlabel('Time')
            i.set_ylabel('#-of Friends Created')
            i.set_title(
                '{} [ {} - {} ]'.format(
                    title,
                    _tmpX[0],
                    _tmpX[-1]
                )
            )

        _fig.savefig(
            sink,
            bbox_inches='tight',
            pad_inches=.5)
        plt.close(_fig)

        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
