#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from matplotlib import pyplot as plt
import seaborn as sns
from ..model.messenger import Messenger
from itertools import chain


def plotTopXBusyChats(data: List[Tuple[str, int]], title: str, sink: str) -> bool:
    '''
        Plotting top X number of busy chats ( in terms
        of number of messages being transacted ) as bar plot
    '''
    if not data:
        return False

    try:
        _x = [i[-1] for i in data]
        _y = [i[0] for i in data]

        with plt.style.context('dark_background'):
            fig = plt.Figure(
                figsize=(16, 9),
                dpi=100)

            sns.barplot(
                x=_x,
                y=_y,
                orient='h',
                ax=fig.gca())

            fig.gca().set_xlabel('# of total Messages in Chat',
                                 labelpad=12)
            fig.gca().set_ylabel('Chat Name',
                                 labelpad=12)
            fig.gca().set_title(title,
                                pad=16,
                                fontsize=20)

            fig.savefig(
                sink,
                bbox_inches='tight',
                pad_inches=.5)
            plt.close(fig)

        return True
    except Exception:
        return False


def _prepareDataForTopXPrivateChatsWithHighestContributonFromYou(messenger: Messenger, x: int, participant: str) -> Tuple[List[str], List[float], List[str], List[str]]:
    '''
        Preparing data to be plotted as grouped bar plot, for top X private
        chats, where you've high participation
    '''
    _data = messenger.topXPrivateChatsWithHighestContributionFromParticipant(
        x,
        participant)

    _x = list(chain.from_iterable(
        [['Rank : {}'.format(i+1)] * 2 for i in range(x)]))
    _y = list(chain.from_iterable([i[2:] for i in _data]))
    _hue = list(chain.from_iterable(
        [['Peer : 1', 'Peer : 2'] for i in range(x)]))
    _names = list(chain.from_iterable([i[:2] for i in _data]))

    return _x, _y, _hue, _names


def plotTopXPrivateChatsWithHighestContributonFromYou(messenger: Messenger, x: int, participant: str, title: str, sink: str) -> bool:
    '''
        Plotting top X private chats, where this user is having highest contribution,
        in terms of # -of messages transacted, as grouped bar plot, where each pair of labels
        along X axis denote a chat happened between them, where left one is this facebook user, and
        other one is his/ her chat peer.
    '''
    if not messenger:
        return False

    try:
        _x, _y, _hue, _names = _prepareDataForTopXPrivateChatsWithHighestContributonFromYou(
            messenger,
            x,
            participant)

        with plt.style.context('dark_background'):
            fig = plt.Figure(
                figsize=(16, 9),
                dpi=100)

            sns.barplot(
                x=_x,
                y=_y,
                hue=_hue,
                palette='Oranges',
                ax=fig.gca())

            _names = list(
                chain.from_iterable(
                    zip(*[_names[i:i+2] for i in range(0, x * 2, 2)])))

            for j, k in enumerate(fig.gca().patches):
                fig.gca().text(k.get_x() + k.get_width() / 2,
                               k.get_y() + k.get_height() * .2 + .1,
                               _names[j],
                               ha='center',
                               rotation=90,
                               fontsize=10,
                               color='black')

            fig.gca().set_ylim(0, 100)
            fig.gca().set_xlabel('Top Ranked Facebook Chats',
                                 labelpad=12)
            fig.gca().set_ylabel('Percentage of Participation in Chat',
                                 labelpad=12)
            fig.gca().set_title(title,
                                pad=16,
                                fontsize=20)

            fig.savefig(
                sink,
                bbox_inches='tight',
                pad_inches=.5)
            plt.close(fig)

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
