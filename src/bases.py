"""Module containing functions to deal with files and prepare the database.
"""


import json
import sys

from common import DATA_DIR, CSV_FILENAME


def read_csv(has_head=True):
    """Reads a CSV file and returns dictionaries for authors and tagnames.

    @param has_head: determines if database file has head. Default True.

    @returns: two dictionaries, authors and tagnames dictionaries.
    """
    csvfile = open('%s%s.csv' % (DATA_DIR, CSV_FILENAME))
    authorsdict = dict()
    tagnamesdict = dict()

    lines = csvfile.readlines()
    if has_head:
        lines = lines[1 : ]

    for line in lines:
        (idAuthor, tagName) = line.split(',')
        idAuthor = int(idAuthor.strip())
        tagName = tagName.strip()

        if idAuthor in authorsdict.keys():
            authorsdict[idAuthor].append(tagName)
        else:
            authorsdict[idAuthor] = [tagName]

        if tagName in tagnamesdict.keys():
            tagnamesdict[tagName].append(idAuthor)
        else:
            tagnamesdict[tagName] = [idAuthor]

    return (authorsdict, tagnamesdict)


def dumpdict(filename, dictionary, path=DATA_DIR):
    """Saves a dictionary in a json file.

    @param filename: name of file without ".json".
    @param dictionary: dictionary to be saved.
    """
    major_version = sys.version_info[0]
    with open('%s%s.json' % (path, filename), 'w') as jsonfile:
        if major_version == 3:
            json.dump(dictionary, jsonfile, ensure_ascii=False, indent=4,
                      sort_keys=True)
        else:
            content = json.dumps(dictionary, ensure_ascii=False, indent=4,
                                 sort_keys=True).encode('utf8')
            jsonfile.write(content)

def loaddict(filename, path=DATA_DIR):
    """Loads a dictionary from a json file.

    @param filename: name of file without ".json".

    @returns: a dictionary.
    """
    dictfile = open('%s%s.json' % (path, filename))
    return json.load(dictfile)