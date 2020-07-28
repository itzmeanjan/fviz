#!/usr/bin/python3

from datetime import datetime
from re import (
    compile as regCompile,
    I as regI
)


class ReactedContent:
    '''
        Holds information related to reaction,
        given by actor to some content on facebook
    '''

    def __init__(self, title: str, reaction: str, actor: str, timestamp: int):
        self._title = title
        self._reaction = reaction
        self._actor = actor
        self._timestamp = timestamp

    @property
    def title(self) -> str:
        return self._title

    @property
    def reaction(self) -> str:
        return self._reaction

    @property
    def actor(self) -> str:
        return self._actor

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)

    @property
    def peer(self) -> str:
        '''
            Returns name of person, whose
            post/ comment/ photo liked by actor
        '''
        if self.reaction == 'LIKE':
            regex = regCompile(r'((likes|liked)\s(.+)\'s)', flags=regI)
            match = regex.search(self.title)
            if not match:
                return None
            return match.group(3)

        regex = regCompile(r'(reacted\sto\s(.+)\'s)', flags=regI)
        match = regex.search(self.title)
        if not match:
            return None
        return match.group(2)

    @property
    def target(self) -> str:
        '''
            Returns target of reaction i.e.
            on which type of content reaction 
            was given

            Content types could possibly be, 
            {comment, post, photo} etc.

            Also includes information where this content
            was present, in case of groups [ i.e. group name ]
        '''
        regex = regCompile(r'(\'s\s(.+))$')

        match = regex.search(self.title)
        if not match:
            return None

        return match.group(2)[:-1]


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
