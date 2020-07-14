#!/usr/bin/python3

from __future__ import annotations
from argparse import ArgumentParser
from typing import Tuple
from os.path import exists, abspath
from .extract import makeDir


def _getCMD() -> Tuple[str, str, str]:
    '''
        Parses command line args, passed while invoking script
    '''
    parser = ArgumentParser()
    parser.add_argument('src',
                        type=str,
                        help='Exported compressed Facebook data as zip file')
    parser.add_argument('extractAt',
                        type=str,
                        help='Extraction location of zip')
    parser.add_argument('sink',
                        type=str,
                        help='Sink directory path, where plots to be placed')
    args = parser.parse_args()

    if not (args.src and args.extractAt and args.sink):
        return None, None, None
    if not (args.src.endswith('.zip') and exists(args.src) and makeDir(abspath(args.sink))):
        return None, None, None

    return tuple(map(lambda e: abspath(e), [args.src, args.extractAt, args.sink]))


def main():
    try:
        src, extractAt, sink = _getCMD()
        if not (src and extractAt and sink):
            raise Exception('Bad CMD args')
    except KeyboardInterrupt:
        print('\n[!] Terminated')
    except Exception as e:
        print('[!] {}'.format(e))


if __name__ == '__main__':
    main()
