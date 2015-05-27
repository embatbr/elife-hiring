"""Module for functions and variables used in other modules.
"""


import json


DATA_DIR = '../data/'


def dumpdict(filename, dictionary):
    with open('%s%s.json' % (DATA_DIR, filename), 'w') as jsonfile:
        json.dump(dictionary, jsonfile, ensure_ascii=False, indent=4, sort_keys=True)

def loaddict(filename):
    dictfile = open('%s%s.json' % (DATA_DIR, filename))
    return json.load(dictfile)