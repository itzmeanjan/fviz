#!/usr/bin/python3

from os.path import exists
from os import mkdir
from zipfile import ZipFile


def makeDir(target: str) -> bool:
    '''
        If a target path doesn't exist, it'll create that directory
    '''
    try:
        if not exists(target):
            mkdir(target)

        return True
    except Exception:
        return False


def extractAll(src: str, sink: str) -> bool:
    '''
        Given path to target zip file, it'll extract all components
        into given target directory
    '''
    if not (exists(src) and src.endswith('.zip') and makeDir(sink)):
        return False

    try:
        zf = ZipFile(src)
        zf.extractall(path=sink)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
