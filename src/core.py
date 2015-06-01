"""Contains the main functions to perform the analysis.
"""

import math
import itertools

from common import TAGNAMES_FILENAME, AUTHORS_FILENAME, MAX_INT
import bases


class ItemsetGenError(Exception):
    """Various types of itemsets generation errors.
    """

    def __init__(self, code):
        """Creates an ItemsetGenError object.

        @param code: determines the type of error.
        """
        if code == 'maxsize':
            self.message = 'The minimum value for maxsize in function gen_itemsets()\
            is 1'


def k_ary_support_count(itemset, tagnamesdict):
    """Calculates the support count for non unitary itemsets.

    @param itemset: the set of items.
    @param tagnamesdict: the dictionary of tagnames.

    @returns: the support count
    """
    X = itemset[0]
    x_list = tagnamesdict[X]
    inter = set(x_list)

    for i in range(1, len(itemset)):
        Y = itemset[i]
        y_list = tagnamesdict[Y]
        inter = inter.intersection(y_list)

    support_count = len(inter)
    return support_count

def gen_itemsets(maxsize=2, minsupport=0):
    """Generates the itemsets obeying to a minimum support condition.

    @param maxsize: maximum size of an itemset. The itemsets created have sizes
    from 1 to maxsize. The minimum value must be 1. Default 2.
    @param minsupport: the minimum value a support must have to the itemset X be
    in the set of valid itemsets. Default 0.

    @returns: the dictionary with itemsets and its respective support counts.
    """
    if maxsize < 1:
        raise ItemsetGenError('maxsize')

    tagnamesdict = bases.loaddict(TAGNAMES_FILENAME)
    authorsdict = bases.loaddict(AUTHORS_FILENAME)
    N = len(authorsdict.keys())
    N_min = math.ceil(minsupport * N)
    tagnames = sorted(tagnamesdict.keys())

    support_counts = dict()
    itemsets = list()

    # unitary itemsets
    for tagname in tagnames:
        support_count = len(tagnamesdict[tagname])
        if support_count > N_min:
            itemsets.append([tagname])
            support_counts[tagname] = support_count

    # k-ary itemsets, with k > 1
    for size in range(1, maxsize):
        new_itemsets = list()

        for i in range(len(itemsets)):
            X = itemsets[i]
            for j in range(i + 1, len(itemsets)):
                Y = itemsets[j]

                if X[ : -1] == Y [ : -1]:
                    newitem = X[ : -1] + [X[-1]] + [Y[-1]]
                    support_count = k_ary_support_count(newitem, tagnamesdict)
                    if support_count > N_min:
                        new_itemsets.append(newitem)
                        newkey = ' & '.join(newitem)
                        support_counts[newkey] = support_count

        itemsets = new_itemsets

    return support_counts


def calc_confidence(itemsets, support_counts, N, separator=-1):
    """Calculates the confidence of a rule for X => Y.

    @param itemsets: the items to calculate the rule.
    @param support_counts: a dictionary of support counts.
    @param N: number of authors.
    @param separator: in which point of itemsets the list is split. Default -1,
    Y = the last element.

    @returns: the confidence
    """
    X = ' & '.join(sorted(itemsets[ : separator]))
    X_and_Y = ' & '.join(sorted(itemsets))

    if X_and_Y in support_counts.keys():
        supp_X_to_Y = support_counts[X_and_Y] / N
        conf_X_to_Y = support_counts[X_and_Y] / support_counts[X] # supports[X] is present if supports[key] is
        return (supp_X_to_Y, conf_X_to_Y)

    return None

def calc_rules(minsupp=0, mincon=0):
    """Returns all rules with confidence of at least mincon.

    @param minsupp: the minimum value for support.
    @param mincon: the minimum value for confidence.

    @returns: the rules
    """
    support_counts = bases.loaddict('support-counts')
    authorsdict = bases.loaddict(AUTHORS_FILENAME)
    N = len(authorsdict.keys())
    rules = dict()

    for supp_key in support_counts.keys():
        keys = supp_key.split(' & ')
        if len(keys) > 1:
            permutations = itertools.permutations(keys)
            for permutation in permutations:
                # repetitions corrected ahead (avoid re-calculation of confidence)
                for separator in range(1, len(permutation)):
                    (supp, conf) = calc_confidence(permutation, support_counts, N,
                                                   separator)

                    if (supp > minsupp) and (conf > mincon):
                        X = ' & '.join(sorted(permutation[ : separator]))
                        Y = ' & '.join(sorted(permutation[separator : ]))
                        rule_key = '%s => %s' % (X, Y)
                        rules[rule_key] = {'support' : supp, 'confidence' : conf}

    return rules