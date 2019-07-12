"""
File: linear_probing_gene_hash_table.py
Author: your name should probably go here

A module to find the genetic similarity between two genomes.
To find how many genes are in common, we use the naive sequential approach.
"""


from classes import Genome, BaseGeneHashTable
## Uncomment the following line to be able to make your own testing Genes
from classes import Gene


class LinearProbingGeneHashTable(BaseGeneHashTable):
    """ A Chaining Gene Hash Table stores Gene objects for efficient
        matching of genes to diseases, meaning faster diagnosis for
        patients. This particular variation makes use of lists to
        handle gene hash collisions.
    """

    def __init__(self, table_size):
        """ Create a hash table of the correct size, reset counters.
        """
        super().__init__(table_size)
        self.hash_table = [None] * table_size

    # ---start student section---
    def insert(self, gene, disease):
        """Inserts the item into the hash table"""
        new_link = (gene, disease)
        index_hash = gene.__hash__() % self.table_size
        self.hashes += 1
        if self.hash_table[index_hash] is None:
            self.hash_table[index_hash] = new_link
        else:
            while self.hash_table[index_hash] is not None:
                old_index_hash = index_hash
                index_hash = (old_index_hash + 1) % self.table_size
            if self.hash_table[index_hash] is None:
                self.hash_table[index_hash] = new_link
            else:
                raise IndexError


    def __getitem__(self, gene):
        """"""
        pass
    # ===end student section===

table = LinearProbingGeneHashTable(4)
table.insert(Gene('atcg'), 'Leukemia')
print(table)
table.insert(Gene('atcg'), 'Leukemia')
print(table)
