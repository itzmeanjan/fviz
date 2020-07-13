#!/usr/bin/python3

from __future__ import annotations
from typing import Dict
from matplotlib import pyplot as plt


def plotReactionCount(data: Dict[str, float], title: str, sink: str) -> bool:
    if not data:
        return False

    try:
        _y = list(data.keys())
        _x = list(data.values())

        with plt.style.context('Solarize_Light2'):
            fig = plt.Figure(figsize=(24, 12), dpi=100)

            plt.barh(range(len(_y)), _x, align='center',
                     color='deepskyblue', lw=1.6)

            plt.yticks(ticks=range(len(_y)), labels=_y)
            plt.xlabel('Percentage of Occurance')
            plt.title(title)

            # fig.tight_layout()
            fig.savefig(sink, bbox_inches='tight', pad_inches=.5)

            plt.close(fig=fig)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
