#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict, Any
from .message import Message
from functools import reduce
from json import load


class Messages:
    '''
        Holder for all messages in a chat ( private/ group )
    '''

    def __init__(self, title: str, participants: Tuple[str], messages: List[Message], active: bool):
        self.title = title
        self._participants = participants
        self._messages = messages
        self.active = active

    @property
    def name(self) -> str:
        return self.title if self.isGroupChat else ' <-> '.join(self.participants)

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
    def isGroupChat(self) -> bool:
        '''
            In a private chat there're two participants,
            if we've more participant, it's a group chat
        '''
        return self.participantCount > 2

    @property
    def groupByParticipant(self) -> Dict[str, int]:
        '''
            Grouping messages by sender, returns a list of sender
            names with their corresponding message contribution count
        '''
        _buffer = dict([(i, 0) for i in self.participants])

        for i in self.messages:
            _buffer[i.sender] = _buffer.get(i.sender, 0) + 1

        return _buffer

    @property
    def getPercentageOfContribution(self) -> Dict[str, float]:
        '''
            Instead of returning number of messages each participant sent
            in chat returns their percentage of contribution
        '''
        return dict([(k, (v / self.count) * 100) for k, v in self.groupByParticipant.items()])

    def getPercentageOfContributionByParticipant(self, participant: str) -> float:
        '''
            Returns of percentage of contribution by participant name
        '''
        return self.groupByParticipant.get(participant, 0) * 100 / self.count

    @staticmethod
    def fromJSON(src: str) -> Messages:
        '''
            Parse JSON data and build messages object, which will
            hold all messages in a chat
        '''

        def _getFileContent() -> Dict[str, Any]:
            with open(src, mode='r') as fd:
                return load(fd)

        data = _getFileContent()
        if len(data['participants']) < 2:
            return None

        return Messages(
            data['title'],
            tuple([i['name'] for i in data['participants']]),
            [Message.fromJSON(i) for i in data['messages']],
            data['is_still_participant'])


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
