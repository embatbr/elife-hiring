#!/usr/bin/python3.4

"""Simple module just to resolve the problem.
@author Eduardo Tenório (embatbr@gmail.com)
"""


from common import DATA_DIR, dumpdict, loaddict


CSV_FILENAME = 'malhacao-tags-users-basket'
AUTHORS_FILENAME = 'authors'
TAGNAMES_FILENAME = 'tagnames'
SUPP_COUNT_FILENAME = 'support-counts'


def read_csv(has_head=True):
    """Reads a CSV file and return a dictionary.

    @param has_head: determines if database file has head (default True).

    @return a dictionary (json format) object.
    """
    csvfile = open('%s%s.csv' % (DATA_DIR, CSV_FILENAME))
    authorsdict = dict()
    tagnamesdict = dict()

    lines = csvfile.readlines()
    if has_head:
        lines = lines[1 : ]

    for line in lines:
        (idAuthor, tagName) = line.split(',')
        idAuthor = int(idAuthor)
        tagName = tagName[ : -1]

        if idAuthor in authorsdict.keys():
            authorsdict[idAuthor].append(tagName)
        else:
            authorsdict[idAuthor] = [tagName]

        if tagName in tagnamesdict.keys():
            tagnamesdict[tagName].append(idAuthor)
        else:
            tagnamesdict[tagName] = [idAuthor]

    return (authorsdict, tagnamesdict)


def support_count():
    tagnamesdict = loaddict(TAGNAMES_FILENAME)
    tagnames = sorted(tagnamesdict.keys())
    bin_itemsets = [(X, Y) for X in tagnames for Y in tagnames if X != Y]

    support_counts = dict()

    # unitary
    for key in tagnames:
        support_counts[key] = len(tagnamesdict[key])

    #binary
    for (X, Y) in bin_itemsets:
        x_list = tagnamesdict[X]
        y_list = tagnamesdict[Y]
        equals = set(x_list).intersection(y_list)
        support_counts['%s + %s' % (X, Y)] = len(equals)

    return support_counts

def association():
    tagnamesdict = loaddict(TAGNAMES_FILENAME)
    tagnames = sorted(tagnamesdict.keys())
    bin_itemsets = [(X, Y) for X in tagnames for Y in tagnames if X != Y]

    authorsdict = loaddict(AUTHORS_FILENAME)
    N = len(authorsdict.keys())
    support_counts = loaddict(SUPP_COUNT_FILENAME)

    supports = dict()
    confidences = dict()
    for (X, Y) in bin_itemsets:
        supp_X_plus_Y = support_counts['%s + %s' % (X, Y)]
        supports['%s => %s' % (X, Y)] = supp_X_plus_Y / N
        confidences['%s => %s' % (X, Y)] = supp_X_plus_Y / support_counts[X]

    return (supports, confidences)


if __name__ == '__main__':
    import sys

    command = sys.argv[1]

    if command == 'extract-csv':
        dictionaries = read_csv()

        filenames = ['authors', 'tagnames']
        for (filename, dictionary) in zip(filenames, dictionaries):
            dumpdict(filename, dictionary)

    elif command == 'support-counts':
        support_counts = support_count()
        dumpdict('support-counts', support_counts)

    elif command == 'association':
        (supports, confidences) = association()
        dumpdict('supports', supports)
        dumpdict('confidences', confidences)