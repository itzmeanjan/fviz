#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict, Set
from datetime import datetime, date, time, timedelta
from os.path import exists
from json import load
from functools import reduce
from .reactedContent import ReactedContent
from operator import sub, add


class Reactions:
    '''
        Holds all reacted content realated information made by an actor
        in form of an ordered listed ( chronologically decreasing )
    '''

    def __init__(self, reactions: List[ReactedContent]):
        self._reactions = reactions

    @property
    def reactions(self) -> List[ReactedContent]:
        '''
            All reactions present under this object
        '''
        return self._reactions

    @property
    def groupByPeers(self) -> Dict[str, List[int]]:
        '''
            Groups all rections by peer name i.e. whose content is
            reacted to, on which ReactedContent instance

            Returns a mapping from peer name to list of ReactedContent indices
        '''
        buffer = {}

        for i, j in enumerate(self.reactions):
            _peer = j.peer
            if not _peer:
                continue

            if _peer not in buffer:
                buffer[_peer] = [i]
                continue

            buffer[_peer].append(i)

        return buffer

    @property
    def peerToReactionCount(self) -> Dict[str, int]:
        '''
            Returns count of interactions made with each peer
            which is extracted from like or reaction.
        '''
        _buffer = {}

        for i in self.reactions:
            _peer = i.peer
            if not _peer:
                continue

            _buffer[_peer] = _buffer.get(_peer, 0) + 1

        return _buffer

    def getTopXPeerToReactionCount(self, x: int) -> Dict[str, int]:
        buffer = self.groupByPeers

        if x >= len(buffer):
            return dict([(k, len(v)) for k, v in buffer.items()])

        return dict([(i, len(buffer[i]))
                     for i in sorted(buffer.keys(), key=lambda e: len(buffer[e]))[-x:]])

    @property
    def groupByReactions(self) -> Dict[str, List[int]]:
        '''
            Groups all reactions by their types i.e. HAHA, SAD, LIKE etc

            Returns a mapping from reaction type to list of reacted content's indices
        '''
        buffer = {}

        for i, j in enumerate(self.reactions):
            _reaction = j.reaction

            if _reaction not in buffer:
                buffer[_reaction] = [i]
                continue

            buffer[_reaction].append(i)

        return buffer

    @property
    def reactionTypeToCount(self) -> Dict[str, int]:
        '''
            Maps reaction types to their corresponding count

            Sum of all counts needs to be strictly equal to
            total number of ReactedContent present under this object
        '''
        buffer = {}

        for i in self.reactions:
            _reaction = i.reaction

            if _reaction not in buffer:
                buffer[_reaction] = 1
                continue

            buffer[_reaction] += 1

        return buffer

    @property
    def reactionTypeToPercentage(self) -> Dict[str, float]:
        '''
            Maps reaction types to their corresponding percentage of presence

            Sum of all percentages needs to be equal to
            100 (approx, cause we're dealing with floats )
        '''
        _count = self.count
        buffer = self.reactionTypeToCount

        for k in buffer:
            buffer[k] = (buffer[k] * 100) / _count

        return buffer

    def getReactionByIndex(self, index: int) -> ReactedContent:
        '''
            Returns ReactedContent object, looked up by
            index of that content in reaction set  
        '''
        if not (index >= 0 and index < self.count):
            return None

        return self._reactions[index]

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
        return self._reactions[-1].time, self._reactions[0].time

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

    @property
    def reactionTypes(self) -> Set[str]:
        '''
            Returns available reaction types
        '''
        return set([i.reaction for i in self.reactions])

    @property
    def reactionTypeToTimeStamps(self) -> Dict[str, List[datetime]]:
        '''
            Groups reactions by their types and 
            returns a mapping of reaction type to list of timestamps,
            when those reactions were made ( in chronological fashion )
        '''
        buffer = self.groupByReactions

        for _, v in buffer.items():
            for i, j in enumerate(v):
                v[i] = self.getReactionByIndex(j).time

        return buffer

    @property
    def dateToReactionTypeAndCount(self) -> Dict[date, Dict[str, int]]:
        '''
            Groups all reacted contents by their date of occurance
            and for each of them keeps track of count of different reactions
            happened on that date
        '''
        buffer = {}

        for i in self.reactions:
            _dt = i.time.date()

            if _dt not in buffer:
                buffer[_dt] = {i.reaction: 1}
            else:
                if i.reaction not in buffer[_dt]:
                    buffer[_dt][i.reaction] = 1
                else:
                    buffer[_dt][i.reaction] += 1

        return buffer

    @property
    def weekToWeekDayAndReactionCount(self) -> Dict[str, Dict[int, int]]:
        '''
            Groups all reactions by week of happening ( where format 
            will be like `Week {x}, {y}` - where `x` is week number of year `y` )
            and along side also keeps track of count of all reactions on 7 possible days
            in each of those weeks
        '''
        buffer = {}

        for i in self.reactions:
            _dt = i.time.date()
            _week = 'Week {}, {}'.format(
                int(_dt.strftime('%W'), base=10) + 1,
                _dt.strftime('%Y'))

            if _week not in buffer:
                buffer[_week] = {
                    int(_dt.strftime('%w'), base=10): 1
                }
            else:
                if int(_dt.strftime('%w'), base=10) not in buffer[_week]:
                    buffer[_week][int(
                        _dt.strftime('%w'),
                        base=10)] = 1
                else:
                    buffer[_week][int(
                        _dt.strftime('%w'),
                        base=10)] += 1

        return buffer

    @property
    def groupByMonth(self) -> Dict[str, List[int]]:
        '''
            Groups all reactions into sublists by
            their month of occurance where month
            will be of form `%b, %Y`
        '''
        buffer = {}

        for i, j in enumerate(self.reactions):
            _month = j.time.strftime('%b, %Y')

            if _month not in buffer:
                buffer[_month] = [i]
            else:
                buffer[_month].append(i)

        return dict([(k, buffer[k]) for k in reversed(buffer.keys())])

    @property
    def reactedContentTypeToCount(self) -> Dict[str, int]:
        '''
            Returns a mapping from reacted content type ( post, photo, comment )
            to their respective count
        '''
        buffer = {}

        for i in self.reactions:
            _contentType = i.target

            if _contentType not in buffer:
                buffer[_contentType] = 1
            else:
                buffer[_contentType] += 1

        return buffer

    @property
    def groupByMinuteInADay(self) -> Dict[time, int]:
        '''
            Maps all reactions into 1440 minutes possible in a day.

            Simply dropping date information from timestamp of occurance of event
            and considering only hour and minute part, keeping track of number of 
            events happened on that minute over time frame of dataset
        '''
        buffer = {}

        for i in self.reactions:
            _tm = i.time.time().replace(second=0)

            if _tm not in buffer:
                buffer[_tm] = 1
            else:
                buffer[_tm] += 1

        return buffer

    @property
    def getInBetweenDelays(self) -> map:
        '''
            Finds all time delays in between any two consecutive like/ reaction
            event, and returns it as a list of timedelta(s)

            For N number of like/ reaction events, N-1 number of timedeltas will
            be there
        '''
        return map(lambda e: sub(
            *sorted((
                self.getReactionByIndex(e-1).time, self.getReactionByIndex(e).time),
                reverse=True)),
            range(1, self.count))

    @property
    def getCumulativeSumOfDelays(self) -> List[timedelta]:
        '''
            Computes cumulative sum of all ascendingly 
            sorted like/ reaction delays 
        '''
        _buffer = sorted(self.getInBetweenDelays)
        _cumsum = []

        for i, j in enumerate(_buffer):

            if not i:
                _cumsum.append(j)
            else:
                _cumsum.append(j + _cumsum[i-1])

        return _cumsum

    @property
    def getCumSumPercentage(self) -> List[float]:
        '''
            Calculate percentage contribution from cum-sum time delays
        '''
        _buffer = self.getCumulativeSumOfDelays
        _percentages = []

        for i in _buffer:
            _percentages.append(i / _buffer[-1] * 100)

        return _percentages

    @property
    def getMeanTimeDelay(self) -> timedelta:
        '''
            Computes mean time delay of all likes/ reactions events
        '''
        _buffer = list(self.getInBetweenDelays)

        return reduce(add, _buffer[1:], _buffer[0]) / len(_buffer)

    @property
    def getMedianTimeDelay(self) -> timedelta:
        '''
            Computes median delay for all like and reaction event
            for this user
        '''
        _buffer = sorted(self.getInBetweenDelays)

        if len(_buffer) % 2 == 0:
            return (_buffer[(len(_buffer) // 2) - 1] + _buffer[len(_buffer) // 2]) / 2
        else:
            return _buffer[len(_buffer) // 2]

    @property
    def groupByWeek(self) -> Dict[str, List[int]]:
        '''
            Groups all like & reaction events by its
            week of happening where week is specified as
            `Week %W, %Y`
        '''
        buffer = {}

        for i, j in enumerate(self.reactions):
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
            Mapping all likes and reactions into their corresponding week of 
            happening where each of them will hold record of which quarter
            of a day is having how many likes and reactions count for that span
            of week

            Gives an idea about how you spent your week on facebook ( scrolling, liking, reacting etc. )
            on which quarter you were mostly active/ inactive and how did that change over time.
        '''
        def mapIntoQuarters(_data: List[int]) -> Dict[str, int]:
            _mappedIntoQuarters = {}

            _06hr = time(6, 0, 0)
            _12hr = time(12, 0, 0)
            _18hr = time(18, 0, 0)

            for i in _data:
                _tm = self.getReactionByIndex(i).time.time()

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

        _buffer = {}

        for k, v in self.groupByWeek.items():
            _buffer[k] = mapIntoQuarters(v)

        return _buffer


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
