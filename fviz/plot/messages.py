#!/usr/bin/python3

from typing import List, Tuple, Dict
from matplotlib import pyplot as plt
import seaborn as sns
from ..model.messenger import Messenger
from itertools import chain
from math import ceil


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
    except Exception:
        return False


def _prepareDataForChatThreadsWithLowestContributonFromYou(messenger: Messenger, x: int, participant: str) -> Tuple[List[str], List[float], List[str], List[str]]:
    '''
        Preparing data to be plotted as grouped bar plot, 
        for private facebook chat threads where you've lowest contribution
    '''
    _data = messenger.topXPrivateChatsWithLowestContributionFromParticipant(
        x,
        participant)

    _x = list(chain.from_iterable(
        [['Least Contributed : {}'.format(i+1)] * 2 for i in range(x)]))
    _y = list(chain.from_iterable([i[2:] for i in _data]))
    _hue = list(chain.from_iterable(
        [['Peer : 1', 'Peer : 2'] for i in range(x)]))
    _names = list(chain.from_iterable([i[:2] for i in _data]))

    return _x, _y, _hue, _names


def plotPrivateChatThreadsWithLowestContributonFromYou(messenger: Messenger, x: int, participant: str, title: str, sink: str) -> bool:
    '''
        Plotting private facebook chat threads, where this user is having lowest contribution,
        in terms of # -of messages transacted, as grouped bar plot, where each pair of labels
        along X axis denote a chat happened between them, where left one is this facebook user, and
        other one is his/ her chat peer.
    '''
    if not messenger:
        return False

    try:
        _x, _y, _hue, _names = _prepareDataForChatThreadsWithLowestContributonFromYou(
            messenger,
            x,
            participant)

        with plt.style.context('dark_background'):
            fig = plt.Figure(
                figsize=(24, 9),
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
            fig.gca().set_xlabel('Least Contributed Facebook Chats',
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
    except Exception:
        return False


def _prepareDataForTopChatThreadEachWeek(messenger: Messenger) -> Tuple[List[str], List[float], List[str], List[str]]:
    '''
        Prepares data for plotting grouped bar chat, for weekly
        top private chat thread.
    '''
    def _orderParticipantsByAscendingContribution(_participants: Dict[str, int]) -> List[str]:
        '''
            Given a dictionary of {str: int} form, sorts keys
            by their corresponding values, ascendingly
        '''
        return sorted(_participants, key=lambda e: _participants[e])

    def _orderParticipantContributionsAscendingly(_participants: Dict[str, int]) -> List[float]:
        '''
            Given a dictionary of {str: int} form, sorts values
            ascendingly, and converts them to percentage of contribution
            by dividing each of them by sum of values in dict and multiplying 
            by 100
        '''
        return list(map(lambda e: (e / sum(_participants.values())) * 100,
                        sorted(_participants.values(),
                               key=lambda e: e)))

    _data = messenger.topChatThreadPerWeek

    _x = list(chain.from_iterable(map(lambda e: [e[0]] * 2, _data)))
    _names = list(
        chain.from_iterable(
            map(lambda e: _orderParticipantsByAscendingContribution(e[1]),
                _data)))
    _hue = list(
        chain.from_iterable(
            map(lambda e: ('Contributor : 1', 'Contributor : 2'),
                _data)))
    _y = list(
        chain.from_iterable(
            map(lambda e: _orderParticipantContributionsAscendingly(e[1]),
                _data)))

    return _x, _y, _hue, _names


def plotTopChatThreadEachWeek(messenger: Messenger, title: str, sink: str) -> bool:
    '''
        Plotting top facebook private chat thread on each week
        when this user was active. This is plotted as a grouped
        bar chart.
    '''
    if not messenger:
        return False

    try:
        _x, _y, _hue, _names = _prepareDataForTopChatThreadEachWeek(messenger)

        sns.set(style='darkgrid')
        _fig, _axes = plt.subplots(
            ceil(len(_x) / 104),
            1,
            figsize=(108, ceil(len(_x) / 104) * 18),
            dpi=100)
        if len(_x) <= 104:
            _axes = [_axes]

        _start = 0
        _end = 104

        for i in _axes:
            _tmpX = _x[_start: _end]
            _tmpY = _y[_start: _end]

            sns.barplot(
                x=_tmpX,
                y=_tmpY,
                hue=_hue[_start: _end],
                palette='YlGn',
                ax=i)

            _tmpNames = _names[_start: _end]
            _tmpNames = list(chain.from_iterable(
                zip(*[_tmpNames[j:j+2] for j in range(0, len(_tmpNames), 2)])))
            _tmpY = list(chain.from_iterable(
                zip(*[_tmpY[j:j+2] for j in range(0, len(_tmpY), 2)])))

            for j, k in enumerate(i.patches):
                i.text(k.get_x() + k.get_width() * .5,
                       k.get_y() + k.get_height() * .36 + k.get_width() * .9,
                       '{} ( {:.2f}% )'.format(_tmpNames[j], _tmpY[j]),
                       ha='center',
                       rotation=90,
                       fontsize=14,
                       color='black')

            i.set_ylim(0, 100)
            i.set_ylabel('Percentage of Participation in Chat')
            i.set_title('{} [ {} - {} ]'.format(
                title,
                _tmpX[0],
                _tmpX[-1]),
                fontsize=20,
                pad=12)
            _start = _end
            _end += 104

        _fig.savefig(
            sink,
            bbox_inches='tight',
            pad_inches=.5)
        plt.close(_fig)

        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
