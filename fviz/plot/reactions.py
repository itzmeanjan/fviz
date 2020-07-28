#!/usr/bin/python3

from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import seaborn as sns
from ..model.reactions import Reactions
from datetime import date, timedelta, time, datetime
from math import ceil
from collections import Counter
from itertools import chain


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


def _getTopXPeersGroupedByMonth(reactions: Reactions,
                                x: int = 3) -> Dict[str, List[Tuple[str, int]]]:
    '''
        Extracts top X peer names ( whose posts were mostly
        liked/ reacted by this actor ) with corresponding
        like and reaction count for each month
    '''

    def _worker(_month: str):
        return Counter(filter(
            lambda e: e,
            [reactions.getReactionByIndex(i).peer for i in groupedByMonth[_month]])).most_common(x)

    groupedByMonth = reactions.groupByMonth
    return dict([(k, _worker(k)) for k in groupedByMonth.keys()])


def _prepareDataForPlottingGroupedBarChartWithTopXPeers(reactions: Reactions,
                                                        x: int = 3) -> Tuple[List[str], List[int], List[str], List[str]]:
    '''
        Preparing data piece by piece for plotting grouped bar chart
        showing top X profiles whose posts were mostly liked and
        reacted in each month over whole time period
    '''
    _topXPeers = _getTopXPeersGroupedByMonth(reactions, x=x)

    _months = _topXPeers.keys()

    _x = list(chain.from_iterable([[i]*x for i in _months]))

    _y = list(chain.from_iterable(
        [[i[-1] for i in _topXPeers[k]] + [0] *
            (x - len(_topXPeers[k])) for k in _months]
    ))
    _hue = list(chain.from_iterable(
        [['1st', '2nd', '3rd'] for i in range(len(_months))]
    ))

    _names = list(chain.from_iterable(
        [[i[0] for i in _topXPeers[k]] + ['NA'] * (x - len(_topXPeers[k]))
         for k in _months]
    ))

    return _x, _y, _hue, _names


def plotTopXPeersByMonth(data: Reactions, title: str, sink: str) -> bool:
    '''
        Plotting top X profiles whose posts were mostly liked and reacted by
        this actor over time frame of this data set, per month basis. Here for simplicity
        keeping X=3.
    '''
    if not data:
        return False

    try:
        _x, _y, _hue, _names = _prepareDataForPlottingGroupedBarChartWithTopXPeers(
            data, x=3)

        sns.set(style='darkgrid')
        _fig, _axes = plt.subplots(
            ceil(len(_x) / 36),
            1,
            figsize=(18, 36),
            dpi=100)

        _start = 0
        _end = 36

        for i in _axes:
            _tmpX = _x[_start: _end]

            sns.barplot(
                x=_tmpX,
                y=_y[_start: _end],
                hue=_hue[_start: _end],
                palette='Greens',
                ax=i)

            _tmpNames = _names[_start: _end]
            _tmpNames = list(chain.from_iterable(
                zip(*[_tmpNames[j:j+3] for j in range(0, len(_tmpNames), 3)])))

            for j, k in enumerate(i.patches):
                i.text(k.get_x() + k.get_width() / 2,
                       k.get_y() + k.get_height() * .2 + .1,
                       _tmpNames[j][:16],
                       ha='center',
                       rotation=90,
                       fontsize=6)

            i.set_ylabel('#-of Likes & Reactions')
            i.set_title('{} [ {} - {} ]'.format(
                title,
                _tmpX[0],
                _tmpX[-1]
            ))
            _start = _end
            _end += 36

        _fig.savefig(
            sink,
            bbox_inches='tight',
            pad_inches=.5)
        plt.close(_fig)

        return True
    except Exception:
        return False


def _prepareDataForPlottingLinePlot(reactions: Reactions) -> Tuple[List[str], List[int]]:
    '''
        Preparing data for plotting line plot showing user activity in minute of day over whole
        time frame of dataset. Returns 1440 element lengthy two data sets, one for plotting across
        X axis and another to plotted across Y axis.
    '''
    _groupedByMinute = reactions.groupByMinuteInADay

    _x = []

    _start = datetime(2000, 1, 1, 0, 0)
    _end = datetime(2000, 1, 1, 23, 59)

    while _start <= _end:
        _x.append(_start.time())
        _start += timedelta(minutes=1)

    _y = [_groupedByMinute.get(i, 0) for i in _x]
    _x = ['{:0>2}:{:0>2}'.format(i.hour, i.minute) for i in _x]

    return _x, _y


def plotAccumulatedUserActivityInEachMinuteOfDay(data: Reactions, title: str, sink: str) -> bool:
    '''
        Maps all likes and reactions onto 24 hr span i.e. 1440 minutes of a day
        and keeps count of them, which is plotted as a line plot
    '''
    if not data:
        return False

    try:
        _x, _y = _prepareDataForPlottingLinePlot(data)

        sns.set(style='darkgrid')

        _fig, _axes = plt.subplots(2, 2, figsize=(40, 16), dpi=100)
        _axes = list(chain.from_iterable(_axes))

        _start = 0
        _end = 360

        for i in _axes:
            _tmpX = _x[_start: _end]

            sns.lineplot(
                x=_tmpX,
                y=_y[_start: _end],
                ax=i
            )

            i.set_xlabel('Time')
            i.set_ylabel('#-of Likes & Reactions')

            _xticks = []
            for j, k in enumerate(_tmpX):
                if k.endswith('00'):
                    _xticks.append(j)

            i.set_xticks(_xticks)
            i.set_xticklabels([_tmpX[i] for i in _xticks])
            # i.tick_params(axis='x', labelrotation=90)
            i.set_title('{} [ {} - {} ]'.format(
                title,
                _tmpX[0],
                _tmpX[-1]
            ))

            _start = _end
            _end += 360

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
