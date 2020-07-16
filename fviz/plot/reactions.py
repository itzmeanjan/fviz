#!/usr/bin/python3

from __future__ import annotations
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import seaborn as sns
from ..model.reactions import Reactions
from datetime import date, timedelta
from math import ceil


def plotReactionCount(data: Dict[str, int], title: str, sink: str) -> bool:
    '''
        Given data holding reaction count for each type of reactions
        plotting it as vertical bar plot, while setting given title,
        and exporting to given sink file
    '''
    if not data:
        return False

    try:
        sns.set(style='darkgrid')
        fig = plt.Figure(figsize=(16, 9), dpi=100)
        sns.barplot(x=list(data.keys()), y=list(
            data.values()), orient='v', ax=fig.gca())

        fig.gca().set_xlabel('Reactions')
        fig.gca().set_ylabel('#-of Occurances')
        fig.gca().set_title(title)

        fig.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)
        return True
    except Exception:
        return False


def plotPeerToReactionCount(data: Dict[str, int], title: str, sink: str) -> bool:
    '''
        Given a dictionary of data holding top X peer 
        name along with their corresponding reaction count, 
        plots that as horizontal bar plot
    '''
    if not data:
        return False

    try:
        sns.set(style='darkgrid')
        fig = plt.Figure(figsize=(16, 9), dpi=100)
        sns.barplot(y=list(data.keys()), x=list(
            data.values()), orient='h', ax=fig.gca())

        fig.gca().set_ylabel('Peer Name')
        fig.gca().set_xlabel('#-of Reactions')
        fig.gca().set_title(title)

        fig.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)
        return True
    except Exception:
        return False


def _prepareHeatMapData(reactions: Reactions) -> Tuple[List[List[int]], List[date], List[str]]:
    '''
        Generates heatmap data, depicting user activity on facebook over whole period of time
        i.e. on which date he/ she put which reaction on a facebook post how many number of times
    '''
    _dates = []

    _start, _end = [i.date() for i in reactions.getTimeFrame]
    while _start <= _end:
        _dates.append(_start)
        _start += timedelta(hours=24)

    _reactionTypes = sorted(list(reactions.reactionTypes))
    _groupedByDate = reactions.dateToReactionTypeAndCount

    buffer = [[] for i in _reactionTypes]

    for i, k in enumerate(_reactionTypes):
        _tmp = buffer[i]

        for j in _dates:
            _tmp.append(_groupedByDate.get(j, {}).get(k, 0))

    return buffer, _dates, _reactionTypes


def plotReactionsOverTimeAsHeatMap(data: Reactions, title: str, sink: str) -> bool:
    def _stripData(_frm: int, _to: int):
        return [i[_frm: _to] for i in _buffer], _dates[_frm: _to]

    if not data:
        return False

    try:
        _buffer, _dates, _reactionTypes = _prepareHeatMapData(data)
        _start = 0
        _end = 365

        fig, _axes = plt.subplots(
            ceil(len(_dates) / 365),
            1,
            figsize=(100, 5 * (ceil(len(_dates) / 365) + 10)),
            dpi=100)

        for i in _axes:

            _tmpBuffer, _tmpDates = _stripData(_start, _end)

            sns.heatmap(
                _tmpBuffer,
                cmap='YlGnBu',
                lw=.5,
                ax=i)

            i.set_xticklabels(
                [k.strftime('%d %b, %Y') for k in _tmpDates],
                rotation=90)
            # i.tick_params(axis='x', which='major', labelsize=6)
            i.set_yticklabels(
                _reactionTypes,
                rotation=0
            )
            i.set_title(
                '{} [ {} - {} ]'.format(
                    title,
                    *[k.strftime('%d %b, %Y') for k in [_tmpDates[0], _tmpDates[-1]]]
                )
            )

            _start = _end
            _end += 365

        fig.savefig(
            sink,
            bbox_inches='tight',
            pad_inches=.5
        )
        plt.close(fig)

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
