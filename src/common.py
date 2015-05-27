"""Module for functions and variables used in other modules.
"""


import json


DATA_DIR = '../data/'


def dumpdict(filename, dictionary):
    """Saves a dictionary in a json file.

    @param filename: name of file without ".json".
    @param dictionary: dictionary to be saved.
    """
    with open('%s%s.json' % (DATA_DIR, filename), 'w') as jsonfile:
        json.dump(dictionary, jsonfile, ensure_ascii=False, indent=4, sort_keys=True)

def loaddict(filename):
    """Loads a dictionary from a json file.

    @param filename: name of file without ".json".

    @returns: a dictionary.
    """
    dictfile = open('%s%s.json' % (DATA_DIR, filename))
    return json.load(dictfile)