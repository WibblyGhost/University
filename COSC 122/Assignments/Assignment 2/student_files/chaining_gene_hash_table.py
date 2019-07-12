"""
File: chaining_gene_hash_table.py
Author: Zachary Sanson

A module to find the genetic similarity between two genomes.
To find how many genes are in common, we use the naive sequential approach.
"""


from classes import GeneLinkedList, GeneLink, BaseGeneHashTable
## Uncomment the following line to be able to make your own testing Genes
# from classes import Gene


class ChainingGeneHashTable(BaseGeneHashTable):
    """ A Chaining Gene Hash Table stores Gene objects for efficient
        matching of genes to diseases, meaning faster diagnosis for
        patients. This particular variation makes use of linked lists
        to handle gene hash collisions.
    """

    def __init__(self, table_size):
        """ Create a hash table of the correct size, reset counters.
            Be sure to use GeneLinkedList objects in your hash table.
        """
        super().__init__(table_size)
        self.hash_table = [GeneLinkedList() for _ in range(table_size)]

    # ---start student section---
    def insert(self, gene, disease):
        """Inserts item into hash table"""
        # Declaring function variables.
        new_link = GeneLink((gene, disease))
        index_hash = gene.__hash__() % self.table_size
        self.hashes += 1
        # If table at index contains nothing, add gene into the table.
        if self.hash_table[index_hash].head is None:
            self.hash_table[index_hash].head = new_link
        # If there are already genes in the table, add gene to the end of the gene_list.
        else:
            current = self.hash_table[index_hash].head
            while current.next_node is not None:
                current = current.next_node
            current.next_node = new_link

    def __getitem__(self, gene):
        """Finds specified item"""
        # Declaring function variables.
        index_hash = gene.__hash__() % self.table_size
        self.hashes += 1
        gene_data_link = self.hash_table[index_hash]
        current = gene_data_link.head
        # Search through the linked list at given index for search-gene.
        while current is not None:
            self.comparisons += 1
            if gene == current.data[0]:
                return current.data[1]
            else:
                current = current.next_node
    # ===end student section===
