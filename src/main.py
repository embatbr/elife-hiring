#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

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
        authorsdict = bases.loaddict(AUTHORS_FILENAME)
        N = len(authorsdict.keys())

        for separator in range(1, len(args)):
            calc = core.calc_confidence(args, support_counts, N, separator)
            if calc is None:
                print('Some of args %s are not present in file "support-counts.json"' % args)
            else:
                X = ' & '.join(sorted(args[ : separator]))
                Y = ' & '.join(sorted(args[separator : ]))

                (supp, conf) = calc
                print('%s => %s\nsupport = %.02f%%\nconfidence = %.02f%%' %
                      (X, Y, supp * 100, conf * 100))

    elif command == 'rules':
        minsupp = float(args[0])
        minconf = float(args[1])

        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)

        print('Calculating rule\nminsupp = %.02f%%\nminconf = %.02f%%' %
              (minsupp * 100, minconf * 100))
        confidences = core.calc_rules(minsupp, minconf)
        bases.dumpdict('confidences_%.02f%%_%.02f%%' % (minsupp * 100, minconf * 100),
                       confidences, path=RESULTS_DIR)