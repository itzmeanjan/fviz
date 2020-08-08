#!/usr/bin/python3

from typing import Dict, Tuple, List
from copy import deepcopy
from ..model.reactions import Reactions
from ..model.comments import Comments
from ..model.messenger import Messenger
from math import ceil
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter


def _mergeWeeklyFacebookActivites(reactions: Reactions, comments: Comments) -> Dict[str, Dict[str, int]]:
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
    _x = list(reversed(data.keys()))
    _y = ['00:00 - 05:59', '06:00 - 11:59', '12:00 - 17:59', '18:00 - 23:59']

    _buffer = [[] for i in range(len(_y))]

    for k in _x:
        _v = data[k]

        for i, j in enumerate(_y):
            _buffer[i].append(_v.get(j, 0))

    return _buffer, _x, _y


def plotWeeklyHeatMapWithLikesReactionsComments(reactions: Reactions, comments: Comments, title: str, sink: str) -> bool:
    '''
        Plotting weekly facebook activity data ( likes, reactions, comments )
        as heatmap, where along X axis active week identifiers are plotted
        and along Y axis quarters of a day are kept. Cells hold visual
        information on how to interpret which quarter was mostly eventful
        in a certain week.
    '''
    def _stripData(_frm: int, _to: int):
        '''
            Stripping subset of data from large 2D dataset
            and tick labels along X axis, given start and end index
        '''
        return [i[_frm: _to] for i in _data], _x[_frm: _to]

    try:
        _data, _x, _y = _prepareDataForPlottingLikeReactionCommentBasedActivities(
            _mergeWeeklyFacebookActivites(reactions, comments))

        if not (_data and _x and _y):
            raise Exception('Unable to prepare data !')

        _frm = 0
        _to = 52

        _fig, _axes = plt.subplots(
            ceil(len(_x) / 52),
            1,
            figsize=(185, 4 * (ceil(len(_x) / 52) + 16)),
            dpi=100)

        for i in _axes:

            _tmpData, _tmpX = _stripData(_frm, _to)

            sns.heatmap(
                _tmpData,
                cmap='PuBu',
                lw=1.0,
                ax=i)

            i.set_xticklabels(
                _tmpX,
                rotation=90)
            i.tick_params(
                axis='x',
                which='major',
                labelsize=10)
            i.set_yticklabels(
                _y,
                rotation=0,
                fontsize=16)
            i.set_title(
                '{} [ {} - {} ]'.format(
                    title,
                    _tmpX[0],
                    _tmpX[-1]),
                pad=16,
                fontsize=30)

            _frm = _to
            _to += 52

        _fig.savefig(
            sink,
            bbox_inches='tight',
            pad_inches=.5)
        plt.close(_fig)

        return True
    except Exception:
        return False


def _mergeAllFacebookPeerActivityCount(reactions: Reactions, comments: Comments, messenger: Messenger, exclude: List[str]) -> Dict[str, int]:
    '''
        For each of like, reaction, comment & messaging - facebook activities,
        we'll accumuate #-of times this account owner has interacted with
        some other facebook profile & return that as an associative array.
    '''
    _buffer = {}

    for i in [reactions.peerToReactionCount, comments.peerToCommentCount, messenger.peerToMessageCount]:
        for k, v in i.items():
            if k in exclude:
                continue

            _buffer[k] = _buffer.get(k, 0) + v

    return _buffer


def _topXHighlyInteractedFacebookPeers(reactions: Reactions, comments: Comments, messenger: Messenger, exclude: List[str], x: int) -> List[Tuple[str, int]]:
    '''
        Get top X highly interacted facebook profiles, in terms of likes, reactions, comments, chatting
    '''
    return Counter(_mergeAllFacebookPeerActivityCount(reactions,
                                                      comments,
                                                      messenger,
                                                      exclude)).most_common(x)


def plotTopXHighlyInteractedFacebookPeers(reactions: Reactions, comments: Comments, messenger: Messenger, exclude: List[str], x: int, title: str, sink: str) -> bool:
    '''
        Given all data extracted from facebook activities of a certain person
        under inspection ( i.e. whose profile being analysed ), it'll first calculate
        how many number of times each profile was interacted with ( finally we'll exclude `self` interactions ),
        which is then used for computing top X most interacted profiles ( may be personal account/ page etc. ),
        which is plotted in form of a nice bar plot
    '''
    if not (reactions and comments and messenger):
        return False

    try:
        _data = _topXHighlyInteractedFacebookPeers(reactions, comments,
                                                   messenger, exclude, x)

        sns.set(style='darkgrid')
        fig = plt.Figure(figsize=(16, 9), dpi=100)

        sns.barplot(x=list(map(lambda e: e[1], _data)),
                    y=list(map(lambda e: e[0], _data)),
                    orient='h', ax=fig.gca(), palette='Blues_d')

        fig.gca().set_xlabel('#-of times interacted with')
        fig.gca().set_ylabel('Facebook Profiles')
        fig.gca().set_title(title)

        fig.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)

        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
