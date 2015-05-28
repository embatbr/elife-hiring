"""Contains the main functions to perform the analysis.
"""

import math

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


def calc_support_count(itemset, tagnamesdict):
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
    """
    if maxsize < 1:
        raise ItemsetGenError('maxsize')

    tagnamesdict = bases.loaddict(TAGNAMES_FILENAME)
    authorsdict = bases.loaddict(AUTHORS_FILENAME)
    N = len(authorsdict.keys())
    N_min = math.ceil(minsupport * N)
    tagnames = sorted(tagnamesdict.keys())

    itemsets_list = [list() for i in range(maxsize)]
    support_count_dict = dict()

    # unitary itemsets
    for tagname in tagnames:
        support_count = len(tagnamesdict[tagname])
        if support_count > N_min:
            itemsets_list[0].append([tagname])
            support_count_dict[tagname] = support_count

    # k-ary itemsets, with k > 1
    for size in range(1, maxsize):
        itemsets = itemsets_list[size - 1]
        for i in range(len(itemsets)):
            X = itemsets[i]
            for j in range(i + 1, len(itemsets)):
                Y = itemsets[j]
                if X[ : -1] == Y [ : -1]:
                    newitem = X[ : -1] + [X[-1]] + [Y[-1]]
                    support_count = calc_support_count(newitem, tagnamesdict)
                    if support_count > N_min:
                        itemsets_list[size].append(newitem)
                        newkey = ' & '.join(newitem)
                        support_count_dict[newkey] = support_count

    return support_count_dict


maxsize = 3
minsupport = 0
support_count_dict = gen_itemsets(maxsize, minsupport)
bases.dumpdict('support_counts', support_count_dict)