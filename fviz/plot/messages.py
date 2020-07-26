#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
from matplotlib import pyplot as plt
import seaborn as sns


def plotTopXBusyChats(data: List[Tuple[str, int]], title: str, sink: str) -> bool:
    '''
        Plotting top X number of busy chats as bar plot in terms
        of number of messages being transacted
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


if __name__ == '__main__':
    print('It\'s not supposed to be used this way !')
