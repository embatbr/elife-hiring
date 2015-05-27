# elife-hiring

Implementation of Association Rule Learning to extract statistics from a CSV file named *malhacao-tags-users-basket.csv*.

The code is composed of a main module (*main.py*) and an auxiliary module (*common.py*). The module *main.py* contains a function *read_csv*, used to extract the data from the CSV file into two different JSON files (*authors.json* and *tagnames.json*). This is done to improve when counting the number of authors/tagnames and which tags/authors they have.

The function *apriori_gen* generates the unitary and binary itemsets, using the **Apriori algorithm** to prune itemsets with a frequency (**support count**) lower than an arbitrary minimum. If the support count is valid, the **support** (support count over total number of authors) is calculated and added to a dictionary of supports. Else, the itemset is removed from the list of itemsets. After this stage, the binary itemsets ("X & Y" from tagnames, where X != Y) are optimally generated (due to the pruning of the earlier stage), and the same process is done (calculate the supports).

The last two functions are *calc_rule*, that creates a rule if the support and the **confidence** are valid (aka, greater of equal to a minimum), and *calc_rules*, that do the same to all tagnames.

The module *main.py* still has an option to receive commands from the console to execute the actions described before.

## Commands

- `extract-csv`: extract data from *malhacao-tags-users-basket.csv* and creates the files *authors.json* and *tagnames.json*, containing dictionaries for authors and tagnames, respectively.

- `rule <X> <Y>`: calculates the rule `<X> => <Y>`.

- `calc-rules [min_supp] [min_conf]`: calculates all rules, given `min_supp` and `min_conf`. These parameters are optional and set to 0 if no present. A file *rules_<min_supp>_<min_conf>* is saved with the rules.