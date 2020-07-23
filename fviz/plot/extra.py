#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
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

    for k, v in comments.weekToQuarterOfDayAndCount:
        _buffer[k] = _buffer.get(k, 0) + v

    return _buffer


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
