#!/usr/bin/python3.4

"""Module to receive commands from terminal and execute actions.
"""


import os, os.path

from common import DATA_DIR, RESULTS_DIR, CSV_FILENAME, AUTHORS_FILENAME
from common import TAGNAMES_FILENAME
import bases
import core


if __name__ == '__main__':
    import sys

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == 'extract-csv':
        print('Extracting CSV files')
        dictionaries = bases.read_csv()

        filenames = ['authors', 'tagnames']
        for (filename, dictionary) in zip(filenames, dictionaries):
            bases.dumpdict(filename, dictionary)

    elif command == 'support-counts':
        maxsize = int(args[0])

        support_counts = core.gen_itemsets(maxsize)
        bases.dumpdict('support-counts', support_counts)

    elif command == 'rule':
        support_counts = bases.loaddict('support-counts')
        for separator in range(1, len(args)):
            confidence = core.calc_confidence(args, support_counts, separator)
            X = ' & '.join(sorted(args[ : separator]))
            Y = ' & '.join(sorted(args[separator : ]))
            print('%s => %s = %.02f%%' % (X, Y, confidence * 100))

    elif command == 'rules':
        minconfidences = map(float, args)

        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)

        for minconfidence in minconfidences:
            print('Calculating rule for minimum confidence %.02f%%' % (minconfidence*100))
            confidences = core.calc_rules(minconfidence)
            bases.dumpdict('confidences_%.02f%%' % (minconfidence * 100), confidences,
                           path=RESULTS_DIR)