"""
File: genetic_similarity_sequential.py
Author: Zachary Sanson

A module to find the genetic similarity between two genomes.
To find how many genes are in common, we use the naive sequential approach.
"""

from classes import GeneList
## Uncomment the following line to be able to make your own testing Genes



def genetic_similarity_sequential(first_genome, second_genome):
    """ This function takes two Genome objects, and returns a GeneList
        and an integer. The GeneList is of all genes that are common
        between first_genome and second_genome, while the integer is how many
        comparisons it took to find all the similar genes.
    """
    common_genes = GeneList()
    comparisons = 0
    for index in first_genome:
        for item in second_genome:
            if index == item:
                comparisons += 1
                common_genes.append(index)
                break
            comparisons += 1
    return common_genes, comparisons
