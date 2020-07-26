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

    def topXBusyChats(self, x: int = 15) -> List[Tuple[str, int]]:
        '''
            Finds top X number of chats with highest number of messages
            transacted
        '''
        return Counter(dict([(i.name, i.count) for i in self._inbox])).most_common(x)

    def topXChatsWithHighestContributionFromParticipant(self, x: int, participant: str) -> List[Tuple[str, int]]:
        '''
            Returns a list ( top X ) of chats where this
            participant ( in general it's you ) made highest contribution
        '''
        return Counter(
            dict([(i.name, i.getPercentageOfContributionByParticipant(participant))
                  for i in self._inbox])).most_common(x)

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
