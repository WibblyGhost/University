"""
File: linear_probing_gene_hash_table.py
Author: Zachary Sanson

A module to find the genetic similarity between two genomes.
To find how many genes are in common, we use the naive sequential approach.
"""


from classes import Genome, BaseGeneHashTable
## Uncomment the following line to be able to make your own testing Genes
#from classes import Gene


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
        # Declaring function variables.
        new_link = (gene, disease)
        index_hash = gene.__hash__() % self.table_size
        original_hash = index_hash
        self.hashes += 1
        while True:
            index = self.hash_table[index_hash]
            # If the table contains nothing at given index, add new item into the table.
            if index is None:
                self.hash_table[index_hash] = new_link
                break
            # Else use linear probing to find the next empty spot.
            index_hash += 1
            index_hash = index_hash % self.table_size
            # If there are no empty spots, return an index error.
            if index_hash == original_hash:
                raise IndexError("Cannot insert any more "
                                 "items into the hash table.")

    def __getitem__(self, gene):
        """Finds disease from given gene"""
        # Declaring function variables.
        index_hash = gene.__hash__() % self.table_size
        original_hash = index_hash
        self.hashes += 1
        while True:
            # If there are no more values in the table to search, return None
            if self.hash_table[index_hash] is None:
                break
            # Else if found a match between search-gene, and table-gene, search found, return the disease.
            elif self.hash_table[index_hash][0] == gene:
                self.comparisons += 1
                return self.hash_table[index_hash][1]
            # Else try look in next position of the table for that gene.
            else:
                self.comparisons += 1
                index_hash = (index_hash + 1) % self.table_size
                # If we have returned to our original hash, search is not found, return None.
                if original_hash == index_hash:
                    break
    # ===end student section===


