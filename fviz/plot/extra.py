#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, Tuple, List
from copy import deepcopy
from ..model.reactions import Reactions
from ..model.comments import Comments


def mergeWeeklyFacebookActivites(reactions: Reactions, comments: Comments) -> Dict[str, Dict[str, int]]:
    '''
        Given seperate weekly likes & reactions activity and 
        comments actvity on Facebook for an user, we can merge them together
        and generate a common data structure holding all like, reaction, comment
        based activities for this user
    '''
    _buffer = deepcopy(reactions.weekToQuarterOfDayAndCount)

    for k, v in comments.weekToQuarterOfDayAndCount.items():
        if k not in _buffer:
            _buffer[k] = v
        else:
            _tmp = _buffer[k]

            for _iK, _iV in v.items():
                _tmp[_iK] = _tmp.get(_iK, 0) + _iV

    return _buffer


def _prepareDataForPlottingLikeReactionCommentBasedActivities(data: Dict[str, Dict[str, int]]) -> Tuple[List[List[int]], List[str], List[str]]:
    '''
        For plotting weekly activity ( facebook likes, reactions, comments ) heatmap with 
        granularity of quarter of day level, data is prepared here

        We need a 2D array holding actual data to be plotted, tick labels 
        along both X axis and Y axis
    '''
    _x = list(data.keys())
    _y = ['00:00 - 05:59', '06:00 - 11:59', '12:00 - 17:59', '18:00 - 23:59']

    _buffer = [[] for i in range(len(_y))]

    for v in data.values():

        for i, j in enumerate(_y):
            _buffer[i].append(v.get(j, 0))

    return _buffer, _x, _y


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
