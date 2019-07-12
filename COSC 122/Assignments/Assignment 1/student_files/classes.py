"""
classes.py
COSC122 Assignment 1 2017

This module provides classes that are to be used to complete the COSC122
Assignment 1. These have many careful restrictions placed on them, but do
provide a sufficient interface to solve the problems given.
"""


from utilities import StatCounter


class Gene(object):
    """ A simple variation on strings so that we can count comparisons.
    """

    def __init__(self, dna):
        if not all(c in {'a', 't', 'c', 'g'} for c in dna):
            raise ValueError(
                'The DNA sequence for this gene is broken: ' + dna)
        self.__dna = dna

    def __repr__(self):
        return repr(self.__dna)

    def __str__(self):
        return str(self.__dna)

    def __eq__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna == other.__dna

    def __le__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna <= other.__dna

    def __ne__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna != other.__dna

    def __lt__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna < other.__dna

    def __gt__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna > other.__dna

    def __ge__(self, other):
        if not isinstance(other, Gene):
            raise ValueError("Gene objects can only be compared "
                             "to other Gene objects")
        StatCounter.inc('comparisons')
        return self.__dna >= other.__dna

    def __hash__(self):
        #StatCounter.inc('hashes')
        if self.__dna is None:
            return 0
        value = ord(self.__dna[0]) << 7
        for char in self.__dna:
            value = self.__c_mul(1000003, value) ^ ord(char)
        value = value ^ len(self.__dna)
        if value == -1:
            value = -2
        return value

    def __c_mul(self, a, b):
        return ((int(a) * int(b)) & 0xFFFFFFFF)


class Genome(object):
    """ A Genome is a list that is immutable.
    """
    _comparisons = 0

    def __init__(self, genes):
        self._genes = list(genes)

    def __repr__(self):
        return ' '.join(str(g) for g in self._genes)

    def __str__(self):
        return ' '.join(str(g) for g in self._genes)

    def __getitem__(self, i):
        StatCounter.inc('accesses')
        return self._genes[i]

    def __len__(self):
        return len(self._genes)

    def __eq__(self, other):
        pre_check_comparisons_count = StatCounter.get('comparisons')
        answer = self._genes == other._genes
        StatCounter.set('comparisons', pre_check_comparisons_count)
        return answer

    def __contains__(self, item):
        raise TypeError(self.__class__.__name__ + " objects "
                        "cannot be used with the 'in' keyword")

    def index(self, item=None):
        raise TypeError(self.__class__.__name__ + " objects "
                        "cannot be searched with 'index'")

    def sort(self):
        raise TypeError(self.__class__.__name__ + " objects "
                        "cannot be sorted with 'sort'")


class GeneList(Genome):
    """ A Gene list is like a Genome, but is mutable
        (i.e., you can append to it).
    """

    def __init__(self):
        super().__init__([])

    def append(self, item):
        if not isinstance(item, Gene):
            raise ValueError("A GeneList can only contain Gene objects")
        self._genes.append(item)
