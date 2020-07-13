#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
from matplotlib import pyplot as plt
import seaborn as sns


def plotReactionCount(data: Dict[str, int], title: str, sink: str) -> bool:
    '''
        Given data holding reaction count for each type of reactions
        plotting it as vertical bar plot, while setting given title,
        and exporting to given sink file
    '''
    if not data:
        return False

    try:
        sns.set(style='darkgrid')
        fig = plt.Figure(figsize=(16, 9), dpi=100)
        sns.barplot(x=list(data.keys()), y=list(
            data.values()), orient='v', ax=fig.gca())

        fig.gca().set_xlabel('Reactions')
        fig.gca().set_ylabel('#-of Occurances')
        fig.gca().set_title(title)

        fig.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)
        return True
    except Exception:
        return False


def plotPeerToReactionCount(data: Dict[str, int], title: str, sink: str) -> bool:
    '''
        Given a dictionary of data holding top X peer 
        name along with their corresponding reaction count, 
        plots that as horizontal bar plot
    '''
    if not data:
        return False

    try:
        sns.set(style='darkgrid')
        fig = plt.Figure(figsize=(16, 9), dpi=100)
        sns.barplot(y=list(data.keys()), x=list(
            data.values()), orient='h', ax=fig.gca())

        fig.gca().set_ylabel('Peer Name')
        fig.gca().set_xlabel('#-of Reactions')
        fig.gca().set_title(title)

        fig.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
