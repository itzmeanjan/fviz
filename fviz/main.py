#!/usr/bin/python3

from __future__ import annotations
from argparse import ArgumentParser
from typing import Tuple
from os.path import exists, abspath
from os import mkdir


def _makeDir(target: str) -> bool:
    '''
        Creates directory at specified path
        if not existing already, denotes 
        success of operation by returning boolean value
    '''
    try:
        if exists(target):
            return True
        mkdir(target)
        return True
    except Exception:
        return False


def _getCMD() -> Tuple[str, str]:
    '''
        Parses command line args, passed while invoking script
    '''
    parser = ArgumentParser()
    parser.add_argument('src',
                        type=str,
                        help='Exported compressed Facebook data as zip file')
    parser.add_argument('sink',
                        type=str,
                        help='Sink directory path, where plots to be placed')
    args = parser.parse_args()

    if not (args.src and args.sink):
        return None, None
    if not (args.src.endswith('.zip') and exists(args.src) and _makeDir(abspath(args.sink))):
        return None, None

    return tuple(map(lambda e: abspath(e), [args.src, args.sink]))


def main():
    print('Under active development ... :)')


if __name__ == '__main__':
    main()
