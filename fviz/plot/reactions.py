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
    '''
        Plots user activity as heatmap showing all reactions
        given by user on facebook posts over time. Each 365 day 
        time span is plotted in its own figure - generating a new image.
    '''
    def _stripData(_frm: int, _to: int):
        '''
            Stripping subset of data from large 2D dataset
            given start and end index
        '''
        return [i[_frm: _to] for i in _buffer], _dates[_frm: _to]

    if not data:
        return False

    try:
        _buffer, _dates, _reactionTypes = _prepareHeatMapData(data)
        _start = 0
        _end = 365

        for i in range(ceil(len(_dates) / 365)):

            fig = plt.Figure(figsize=(100, 2), dpi=100)

            _tmpBuffer, _tmpDates = _stripData(_start, _end)

            sns.heatmap(
                _tmpBuffer,
                cmap='YlGnBu',
                lw=.75,
                ax=fig.gca())

            fig.gca().set_xticklabels(
                [k.strftime('%d %b, %Y') for k in _tmpDates],
                rotation=90)
            fig.gca().tick_params(
                axis='x',
                which='major',
                labelsize=6)
            fig.gca().set_yticklabels(
                _reactionTypes,
                rotation=0)
            fig.gca().set_title(
                '{} [ {} - {} ]'.format(
                    title,
                    *[k.strftime('%d %b, %Y') for k in [_tmpDates[0], _tmpDates[-1]]]),
                pad=12)
            fig.gca().set_xlabel('Dates')
            fig.gca().set_ylabel('Reactions')

            fig.savefig(
                '{}_{}.svg'.format(sink, i),
                bbox_inches='tight',
                pad_inches=.5)
            plt.close(fig)

            _start = _end
            _end += 365

        return True
    except Exception:
        return False


def _prepareWeeklyReactionHeatMapData(reactions: Reactions) -> Tuple[List[List[int]], List[str], List[str]]:
    '''
        Groups reactions by their week of happening and builds a 2D array
        holding information on which weekday of which week of which year 
        how many reactions were recorded ( tries to capture all reaction type 
        activities on facebook )

        Along with that also returns a list of possible week names
        spanning across time frame of dataset, which is going to be
        used as ticklabels of X axis. 

        For Y axis ticklabels, we'll be using week day names i.e. Sunday, Monday etc.
    '''
    _weeks = []
    _start, _end = [i.date() for i in reactions.getTimeFrame]

    while _start <= _end:
        _weeks.append('Week {}, {}'.format(
            int(_start.strftime('%W'),
                base=10) + 1,
            _start.strftime('%Y')))
        _start += timedelta(days=7)

    if 'Week {}, {}'.format(int(_end.strftime('%W'), base=10) + 1, _end.strftime('%Y')) not in _weeks:
        _weeks.append('Week {}, {}'.format(
            int(_end.strftime('%W'), base=10) + 1, _end.strftime('%Y')))

    _groupedByWeek = reactions.weekToWeekDayAndReactionCount
    _buffer = [[] for i in range(7)]

    for i in range(7):
        _tmp = _buffer[i]

        for j in _weeks:
            _tmp.append(_groupedByWeek.get(j, {}).get(i, 0))

    return _buffer, _weeks, ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


def plotWeeklyReactionHeatMap(data: Reactions, title: str, sink: str) -> bool:
    '''
        Plotting like(s) and reaction(s) on facebook data as github style
        activity heatmap, where along Y-axis we keep week day names
        and along X-axis we keep week identifiers. And in cells we put accumulated
        reaction count that day of that week, considering all reaction types.
    '''
    def _stripData(_frm: int, _to: int) -> Tuple[List[List[int]], List[str]]:
        '''
            Stripping subset of data from large 2D dataset
            given start and end index
        '''
        return [i[_frm: _to] for i in _buffer], _weeks[_frm: _to]

    if not data:
        return False

    try:
        _buffer, _weeks, _weekDays = _prepareWeeklyReactionHeatMapData(data)
        _start = 0
        _end = 52

        _fig, _axes = plt.subplots(
            ceil(len(_weeks) / 52),
            1,
            figsize=(60, 4 * (ceil(len(_weeks) / 52) + 15)),
            dpi=100)

        for i in _axes:

            _tmpBuffer, _tmpWeeks = _stripData(_start, _end)

            sns.heatmap(
                _tmpBuffer,
                cmap='YlGnBu',
                lw=.75,
                ax=i)

            i.set_xticklabels(
                _tmpWeeks,
                rotation=90)
            i.tick_params(
                axis='x',
                which='major',
                labelsize=6)
            i.set_yticklabels(
                _weekDays,
                rotation=0)
            i.set_title(
                '{} [ {} - {} ]'.format(
                    title,
                    _tmpWeeks[0],
                    _tmpWeeks[-1]),
                pad=12)

            _start = _end
            _end += 52

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
