#!/usr/bin/python3

from ..model.comments import Comments
import seaborn as sns
from matplotlib import pyplot as plt


def plotTopXPeersWithMostCommentedPostsByUser(data: Comments, title: str, sink: str) -> bool:
    '''
        Finds out those facebook profiles who are
        mostly involved in this person's
        comment history, and plots them
        with their name & respective count of involvements
    '''
    if not data:
        return False

    try:
        _topXPeers = data.topXPeersWithMostInvolvementInComments()
        _x = [i[0] for i in _topXPeers]
        _y = [i[1] for i in _topXPeers]

        with plt.style.context("dark_background"):
            fig = plt.Figure(
                figsize=(16, 9),
                dpi=100)

            sns.barplot(x=_y,
                        y=_x,
                        orient='h',
                        ax=fig.gca())

            fig.gca().set_xlabel('#-of Involvements')
            fig.gca().set_ylabel('Facebook Profiles')
            fig.gca().set_title(title)

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
