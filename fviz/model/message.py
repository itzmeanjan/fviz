#!/usr/bin/python3

from __future__ import annotations
from datetime import datetime
from typing import Dict, Any


class Message:
    '''
        Data class for holding information about a certain message
        sent by a chat participant
    '''

    def __init__(self, sender: str, timestamp: int, content: str, _type: str):
        self.sender = sender
        self._timestamp = timestamp
        self.content = content
        self.type = _type

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)

    @staticmethod
    def fromJSON(data: Dict[str, Any]) -> Message:
        return Message(data['sender_name'],
                       data['timestamp_ms']/1000,
                       data.get('content'),
                       data.get('type'))


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
