#!/usr/bin/python3.4

"""Simple module just to resolve the problem.
@author Eduardo Tenório (embatbr@gmail.com)
"""


from common import DATA_DIR, dumpdict, loaddict


CSV_FILENAME = 'malhacao-tags-users-basket'
AUTHORS_FILENAME = 'authors'
TAGNAMES_FILENAME = 'tagnames'


def read_csv(has_head=True):
    """Reads a CSV file and returns dictionaries for authors and tagnames.

    @param has_head: determines if database file has head (default True).

    @returns: two dictionaries: a authors dictionary and a tagnames dictionary.
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


def apriori_gen(min_supp=0):
    """Calculates the frequency of occurrencies of itemsets in the authors' set.
    Each tagname can be viewed as a bit in a string of bits with "1" indicating
    presence and "0", absence. So, if X and Y are tagnames here (a simple ruler),
    X + Y means the presence of both, and its support count means to count in which
    authors both are present. This is done by intersecting the lists of users from
    both tagnames in tagnames.json.

    The Apriori algorithm for pruning is performed beautifully to generate the
    itemsets and the supports.

    @param min_supp: minimum value for support. Default, 0.

    @returns: a dictionary containing the number of occurrencies for each tagname
    as well as for each tuple of different tagnames.
    """
    tagnamesdict = loaddict(TAGNAMES_FILENAME)
    tagnames = sorted(tagnamesdict.keys())
    supports = dict()
    authorsdict = loaddict(AUTHORS_FILENAME)
    N = len(authorsdict.keys())
    N_min = int(min_supp * N) # used to avoid divide every supp_count by N, even when discarded

    # unitary
    for key in tagnames[:]:
        supp = len(tagnamesdict[key])
        if supp >= N_min:
            supports[key] = supp / N
        else:
            tagnames.remove(key)

    # cross-product (without repetition) of the remaining items
    bin_itemsets = list()
    for i in range(len(tagnames)):
        X = tagnames[i]
        for j in range(i + 1, len(tagnames)):
            Y = tagnames[j]
            bin_itemsets.append((X, Y))

    #binary
    for (X, Y) in bin_itemsets[:]:
        x_list = tagnamesdict[X]
        y_list = tagnamesdict[Y]
        x_and_y = set(x_list).intersection(y_list)

        supp = len(x_and_y)
        if supp >= N_min:
            supports['%s & %s' % (X, Y)] = supp / N
        else:
            bin_itemsets.remove((X, Y))

    return (supports, bin_itemsets)

def calc_rule(X, Y, supports, min_conf=0):
    """Calculate a rule for X and Y.

    @param X: the antecedent.
    @param Y: the consequent.
    @param supports: a dictionary containing all support counts.
    @param min_conf: minimum value for confidence.

    @returns: a rule, if existent, or None otherwise.
    """
    key = '%s & %s' % ((X, Y) if X <= Y else (Y, X))
    if key in supports.keys():
        supp = supports[key]
        conf_X_to_Y = supp / supports[X] # supports[X] is present if supports[key] is

        if conf_X_to_Y >= min_conf:
            key = '%s => %s' % (X, Y)
            rule = dict()
            rule['support'] = supp
            rule['confidence'] = conf_X_to_Y
            return rule

    return None

def calc_rules(min_supp=0, min_conf=0):
    """Calculates all rules.

    @param min_supp: minimum value for support.
    @param min_conf: minimum value for confidence.

    @returns: the dictionary of rules.
    """
    tagnamesdict = loaddict(TAGNAMES_FILENAME)
    tagnames = sorted(tagnamesdict.keys())

    (supports, bin_itemsets) = apriori_gen(min_supp)
    rules = dict()
    for (X, Y) in bin_itemsets:
        for (antecedent, consequent) in [(X, Y), (Y, X)]:
            rule = calc_rule(antecedent, consequent, supports, min_conf)
            if not (rule is None):
                rules['%s => %s' % (antecedent, consequent)] = rule

    return rules


if __name__ == '__main__':
    import sys

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == 'extract-csv':
        print('Extracting CSV files')
        dictionaries = read_csv()

        filenames = ['authors', 'tagnames']
        for (filename, dictionary) in zip(filenames, dictionaries):
            dumpdict(filename, dictionary)

    elif command == 'rule':
        X = args[0]
        Y = args[1]

        authorsdict = loaddict(AUTHORS_FILENAME)
        supports = apriori_gen()[0]
        rule = calc_rule(X, Y, supports)

        key = '%s => %s' % (X, Y)
        print('%s' % key)
        print('support = %.02f%%' % (rule['support']*100))
        print('confidence = %.02f%%' % (rule['confidence']*100))

    elif command == 'calc-rules':
        min_supp = float(args[0]) if len(args) > 0 else 0
        min_conf = float(args[1]) if len(args) > 1 else 0

        print('Calculating rules')
        print('min_supp = %.02f%%' % (min_supp*100))
        print('min_conf = %.02f%%' % (min_conf*100))

        rules = calc_rules(min_supp, min_conf)
        dumpdict('rules_%.02f_%.02f' % (min_supp*100, min_conf*100), rules)