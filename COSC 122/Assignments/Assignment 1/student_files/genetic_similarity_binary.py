"""
File: genetic_similarity_binary.py
Author: Zach

A module to find the genetic similarity between two genomes.
To find how many genes are in common, we use a binary index
"""


from classes import GeneList
## Uncomment the following line to be able to make your own testing Genes
## from classes import Gene, Genome


def genetic_similarity_binary(first_genome, second_genome):
    """ This function takes two Genome objects, and returns a GeneList
        and an integer. The GeneList is of all genes that are common
        between first_genome and second_genome, while the integer is
        how many comparisons it took to find all the similar genes.
        Hint: it might pay to define a helper function.
    """
    comparisons = 0
    common_genes = GeneList()
    for index in first_genome:
        upper = len(second_genome) - 1
        lower = 0
        while upper > lower:
            mid = (upper + lower) // 2
            comparisons += 1
            if index <= second_genome[mid]:
                upper = mid
            else:
                lower = mid + 1
        mid = (upper + lower) // 2
        comparisons += 1

        if second_genome[mid] == index:
            common_genes.append(index)
    return common_genes, comparisons
