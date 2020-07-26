#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict, Any
from .message import Message


class Messages:
    '''
        Holder for all messages in a chat ( private/ group )
    '''

    def __init__(self, participants: Tuple[str], messages: List[Message], active: bool):
        self._messages = messages

    @property
    def messages(self) -> List[Message]:
        return self._messages

    @property
    def count(self) -> int:
        return len(self._messages)

    def byIndex(self, _idx: int) -> Message:
        return self._messages[_idx] if _idx >= 0 and _idx < self.count else None

    @staticmethod
    def fromJSON(data: Dict[str, Any]) -> Messages:
        return Messages(
            tuple([i['name'] for i in data[['participants']]]),
            [Message.fromJSON(i) for i in data['messages']],
            data['is_still_participant'])


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
