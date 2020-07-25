#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
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


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
