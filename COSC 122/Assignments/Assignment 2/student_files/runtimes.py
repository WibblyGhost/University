"""
runtimes.py
Author: Aaron Stockdill

This script collects information about your code for the large dataset
and presents the results as a graph.
"""

import matplotlib.pyplot as plt
import time

from classes import Gene, Genome, GeneList, GeneLinkedList, GeneLink, BaseGeneHashTable
from utilities import StatCounter, read_test_data

from chaining_gene_hash_table import ChainingGeneHashTable
from linear_probing_gene_hash_table import LinearProbingGeneHashTable


def plot_data(name, chaining, probing):
    plt.title("Comparison of table load and {}".format(name.lower()))
    plt.xlabel("Table load")
    plt.ylabel(name)
    plt.plot(*zip(*chaining), label="Chaining")
    plt.plot(*zip(*probing), label="Linear Probing")
    plt.legend()
    plt.show()


def run_disease_checker(table_size, disease_information, patient,
                        hash_table_class):
    start = time.time()
    table = hash_table_class(table_size)
    diseases = set()
    for entry in disease_information:
        table.insert(*entry)
    for gene in patient:
        disease = table[gene]
        if disease is not None:
            diseases.add(disease)
    return (diseases, table.comparisons, time.time() - start)


def run_tests(file_names, hash_table_class):
    comp_info = []
    time_info = []
    for file_name in file_names:
        (table_size,
         disease_information,
         patient,
         true_answer) = read_test_data(file_name)
        _, comps, times = run_disease_checker(table_size,
                                              disease_information,
                                              patient,
                                              hash_table_class)
        load = len(disease_information) / table_size
        comp_info.append((load, comps))
        time_info.append((load, times))
    comp_info.sort()
    return comp_info, time_info


def main():
    file_names = [
        "TestData/test_data-176-176-50.txt",
        "TestData/test_data-200-176-50.txt",
        "TestData/test_data-300-176-50.txt",
        "TestData/test_data-400-176-50.txt",
        "TestData/test_data-900-176-50.txt"
    ]
    chaining_info = run_tests(file_names, ChainingGeneHashTable)
    probing_info = run_tests(file_names, LinearProbingGeneHashTable)
    # Uncomment one of the following lines at a time
    plot_data("Comparisons", chaining_info[0], probing_info[0])
    # plot_data("Time", chaining_info[1], probing_info[1])


main()
