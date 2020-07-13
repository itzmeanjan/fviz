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
        fig = plt.Figure(figsize=(16, 9), dpi=100)

        sns.set(style='darkgrid')
        sns.barplot(x=list(data.keys()), y=list(data.values()), orient='v')
        plt.xlabel('Reactions')
        plt.ylabel('#-of Occurances')
        plt.title(title)

        plt.savefig(sink, bbox_inches='tight', pad_inches=.5)
        plt.close(fig)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
