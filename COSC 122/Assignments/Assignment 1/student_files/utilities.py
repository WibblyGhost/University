"""
utilities.py
A collection of useful structures to complete this assignment.
"""

import random
import struct


GENE_LENGTH = 16


class StatCounter(object):
    """ This class is never initialised, it is just used to
        hold some useful information about comparisons.
    """

    __dict = {
        'comparisons': 0,
        'accesses': 0,
    }

    def __init__(self, *args, **kwargs):
        raise TypeError("The GeneCounter class should never be initialized!")

    @classmethod
    def inc(cls, name):
        cls.__dict[name] += 1

    @classmethod
    def get(cls, name):
        return cls.__dict[name]

    @classmethod
    def set(cls, name, value):
        cls.__dict[name] = value

    @classmethod
    def reset(cls, name):
        cls.__dict[name] = 0


class GeneSequenceGenerator(object):
    """ Generate a sequence of genes
    """

    def __init__(self, max_size=None):
        self.max_size = max_size if max_size is not None else float('inf')

    def __iter__(self):
        from classes import Gene
        i = 0
        while i < self.max_size:
            gene = ''
            for _ in range(GENE_LENGTH):
                gene += random.choice('acgt')
            yield Gene(gene)
            i += 1


def take(sequence, n):
    """ Take the first min(n, len(sequence)) items from sequence. """
    i = 0
    seq = iter(sequence)
    while seq and i < n:
        yield next(seq)
        i += 1


# To use the Gene Sequence Generator:
# >>> from utilities import *
# >>> genes = take(GeneSequenceGenerator(), 10)
# >>> print(list(genes))


def read_test_data(filename):
    """ Read in the test data from the file given by filename.
    """
    from classes import Gene, Genome, GeneList   # Do here, to avoid Circular imports
    with open(filename) as f:
        genome_string_1, genome_string_2, genome_string_3 = [
            l.strip() for l in f.readlines()]
    genome_1 = Genome(_chunk_and_genify(genome_string_1, Gene))
    genome_2 = Genome(_chunk_and_genify(genome_string_2, Gene))
    common_genes = GeneList()
    [common_genes.append(c) for c in _chunk_and_genify(genome_string_3, Gene)]
    return genome_1, genome_2, common_genes


def _chunk_and_genify(sequence, geneifier):
    """ Turn a sequence of bases into a list of Genes.
    """
    genome_list = []
    chunks = iter(sequence[i:i + GENE_LENGTH]
                  for i in range(0, len(sequence), GENE_LENGTH))
    return [geneifier(c) for c in chunks]
