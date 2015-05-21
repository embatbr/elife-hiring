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
    authordict = dict()
    tagnamedict = dict()

    lines = csvfile.readlines()
    if hashead:
        lines = lines[1 : ]

    for line in lines:
        (idAuthor, tagName) = line.split(',')
        idAuthor = int(idAuthor)
        tagName = tagName[ : -1]

        if idAuthor in authordict.keys():
            authordict[idAuthor].append(tagName)
        else:
            authordict[idAuthor] = [tagName]

        if tagName in tagnamedict.keys():
            tagnamedict[tagName].append(idAuthor)
        else:
            tagnamedict[tagName] = [idAuthor]

    return (authordict, tagnamedict)


if __name__ == '__main__':
    import sys

    filename = 'malhacao-tags-users-basket'

    command = sys.argv[1]

    if command == 'extract-base':
        (authordict, tagnamedict) = read_csv(filename)

        AUTHOR_FILE_PATH = '%sauthors.json' % DATA_DIR
        with open(AUTHOR_FILE_PATH, 'w') as authorfile:
            json.dump(authordict, authorfile, ensure_ascii=False, indent=4,
                      sort_keys=True)

        TAGNAME_FILE_PATH = '%stagnames.json' % DATA_DIR
        with open(TAGNAME_FILE_PATH, 'w') as tagnamefile:
            json.dump(tagnamedict, tagnamefile, ensure_ascii=False, indent=4,
                      sort_keys=True)