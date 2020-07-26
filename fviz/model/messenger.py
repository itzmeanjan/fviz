#!/usr/bin/python3

from __future__ import annotations
from .messages import Messages
from typing import List, Dict, Any, Tuple
from json import load
from functools import reduce
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count
from collections import Counter


class Messenger:
    def __init__(self, inbox: List[Messages]):
        self._inbox = inbox

    @property
    def inbox(self) -> List[Messages]:
        return self._inbox

    @property
    def count(self) -> int:
        return len(self._inbox)

    def byIndex(self, _idx: int) -> Messages:
        return self._inbox[_idx] if _idx >= 0 and _idx < self.count else None

    def topXBusiestChats(self, x: int = 15) -> List[Tuple[str, int]]:
        '''
            Finds top X number of chats with highest number of messages
            transacted
        '''
        return Counter(dict([(i.name, i.count) for i in self._inbox])).most_common(x)

    def topXPrivateChatsWithHighestContributionFromParticipant(self, x: int, participant: str) -> List[Tuple[str, int]]:
        '''
            Returns a list ( top X ) of busiest private chats where this
            participant ( yes it's you ) made highest contribution
        '''

        def _organizeParticipants(_participants: Tuple[str]) -> Tuple[str]:
            return _participants if _participants[0] == participant \
                else (_participants[1], _participants[0])

        return list(
            map(lambda e: (e[0], e[1], e[-1], 100 - e[-1]),
                sorted(
                sorted(
                    map(
                        lambda e: (*_organizeParticipants(e.participants),
                                   e.count,
                                   e.getPercentageOfContributionByParticipant(participant)),
                        filter(lambda e: e.participantCount == 2,
                               self._inbox)),
                    key=lambda e: e[-1] * e[-2],
                    reverse=True)[:x],
                key=lambda e: e[-1],
                reverse=True)))

    @staticmethod
    def fromJSON(src: List[str]) -> Messenger:
        '''
           Reads each JSON file content concurrently, holding messages
           and objectifies them, finally forming Messenger object,
           which can be manipulated later
        '''
        try:
            with ThreadPoolExecutor(cpu_count() or 1) as _exec:
                return Messenger(
                    list(
                        filter(lambda e: e,
                               map(lambda e: e.result(),
                                   as_completed(
                                   [_exec.submit(Messages.fromJSON, src=i)
                                    for i in src]
                               )))))
        except Exception:
            return None


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
