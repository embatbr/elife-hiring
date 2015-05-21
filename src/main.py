#!/usr/bin/python3.4

"""Simple module just to resolve the problem.
@author Eduardo Tenório (embatbr@gmail.com)
"""


import json
from common import DATA_DIR


def read_csv(filename, hashead=True):
    """Reads a CSV file and return a dictionary.

    @param filename: name of the database file.
    @param hashead: determines if database file has head (default True).

    @return a dictionary (json format) object.
    """
    csvfile = open('%s%s.csv' % (DATA_DIR, filename))
    datadict = dict()

    lines = csvfile.readlines()
    if hashead:
        lines = lines[1 : ]

    for line in lines:
        (idAuthor, tagName) = line.split(',')
        idAuthor = int(idAuthor)
        tagName = tagName[ : -1]

        if idAuthor in datadict.keys():
            datadict[idAuthor].append(tagName)
        else:
            datadict[idAuthor] = [tagName]

    return datadict


if __name__ == '__main__':
    import sys

    filename = 'malhacao-tags-users-basket'

    command = sys.argv[1]

    if command == 'extract-base':
        datadict = read_csv(filename)

        DATA_FILE_PATH = '%s%s.json' % (DATA_DIR, filename)
        with open(DATA_FILE_PATH, 'w') as datafile:
            json.dump(datadict, datafile, ensure_ascii=False, indent=4, sort_keys=True)