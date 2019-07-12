"""
classes.py
COSC122 Assignment 2 2017

This module provides classes that are to be used to complete the COSC122
Assignment 2. These have many careful restrictions placed on them, but do
provide a sufficient interface to solve the problems given.
"""


from utilities import StatCounter
from abc import ABC, abstractmethod


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
        if other is None:
            StatCounter.inc('comparisons')
            return False
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
        if other is None:
            StatCounter.inc('comparisons')
            return False
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
        StatCounter.inc('hashes')
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

    def __init__(self, genes):
        self._genes = list(genes)

    def __repr__(self):
        return ' '.join(map(str, self._genes))

    def __str__(self):
        return ' '.join(map(str, self._genes))

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

    def append(self):
        raise TypeError(self.__class__.__name__ + " objects "
                        "cannot be appended to")


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


class GeneLink(object):
    """ A single link in a GeneLinkedList. It has two attributes:
        data, which is a Gene object; and next_node, which is pointer to
        another GeneLink.
    """

    def __init__(self, data):
        self.data = data
        self.next_node = None

    def __str__(self):
        return "({})".format(str(self.data)) + " -> " + str(self.next_node)


class GeneLinkedList(object):
    """ A linked list of GeneLinks.
    """

    def __init__(self):
        self.head = None

    def __iter__(self):
        raise ValueError("It would be no fun if we did this for you!")

    def __str__(self):
        return str(self.head)


class BaseGeneHashTable(ABC):
    """ The base class for all the hash tables you are going to implement
        in this part of the assignment. You should subclass this base class
        to make sure you have access to all the methods that we provide.

        FYI: ABC stands for abstract base class.
    """

    @abstractmethod
    def __init__(self, table_size):
        self.table_size = table_size
        self.comparisons = 0
        self.hashes = 0
        # remember to define self.hash_table

    @abstractmethod
    def __getitem__(self, gene):
        pass

    @abstractmethod
    def insert(self, gene, disease):
        pass

    def __str__(self):
        results = []
        for i, row in enumerate(self.hash_table):
            results.append("  {}: {}".format(i, str(row)))
        results = [self.__class__.__name__ + "["] + results + ["]"]
        return "\n".join(results)
