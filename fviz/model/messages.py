#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict, Any
from .message import Message
from collections import Counter
from functools import reduce


class Messages:
    '''
        Holder for all messages in a chat ( private/ group )
    '''

    def __init__(self, participants: Tuple[str], messages: List[Message], active: bool):
        self._participants = participants
        self._messages = messages
        self.active = active

    @property
    def messages(self) -> List[Message]:
        return self._messages

    @property
    def count(self) -> int:
        return len(self._messages)

    @property
    def participantCount(self) -> int:
        return len(self._participants)

    @property
    def participants(self) -> Tuple[str]:
        return self._participants

    def byIndex(self, _idx: int) -> Message:
        return self._messages[_idx] if _idx >= 0 and _idx < self.count else None

    @property
    def groupByParticipant(self) -> Dict[str, int]:
        '''
            Grouping messages by sender, returns a list of sender
            names with their corresponding message contribution count
        '''
        _buffer = dict([(i, 0) for i in self.participants])

        for i in self.messages:
            _buffer[i.sender] += 1

        return _buffer

    @staticmethod
    def fromJSON(data: Dict[str, Any]) -> Messages:
        '''
            Parse JSON data and build messages object, which will
            hold all messages in a chat
        '''
        if len(data['participants']) < 2:
            return None

        return Messages(
            tuple([i['name'] for i in data['participants']]),
            [Message.fromJSON(i) for i in data['messages']],
            data['is_still_participant'])


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
