"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""

import unittest
import math

from classes import Gene, Genome, GeneList, GeneLinkedList, GeneLink, BaseGeneHashTable
from utilities import StatCounter, read_test_data

from chaining_gene_hash_table import ChainingGeneHashTable
from linear_probing_gene_hash_table import LinearProbingGeneHashTable


TEST_FILE_FORMAT = "TestData/test_data-{table}-{db}-{present}.txt"


class BaseTestGeneLookup(unittest.TestCase):

    def setUp(self):
        """Runs before every test case"""
        for counter in {'comparisons', 'accesses', 'hashes', 'memory'}:
            StatCounter.reset(counter)

    def get_bounds(self, table_size, gene_count, patient_genome_length,
                   bad_gene_count, scale):
        lower_bound = bad_gene_count
        upper_bound = patient_genome_length * \
            int(scale * gene_count * gene_count / table_size)
        return lower_bound, upper_bound

    def run_disease_checker(self, table_size, disease_information, patient,
                            hash_table_class):
        table = hash_table_class(table_size)
        diseases = set()
        for entry in disease_information:
            table.insert(*entry)
        for gene in patient:
            disease = table[gene]
            if disease is not None:
                diseases.add(disease)
        return (diseases, table.comparisons, table.hashes)

    def common_genes_test(self, test_file_name):
        """ Test that the given hash table returns the correct
            result for the file specified by test_file_name.
        """
        (table_size,
         disease_information,
         patient,
         true_answer) = read_test_data(test_file_name)
        student_answer, _, _ = self.run_disease_checker(table_size,
                                                        disease_information,
                                                        patient)
        self.assertEqual(student_answer, true_answer)

    def internal_comparisons_test(self, test_file_name):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
        """
        (table_size,
         disease_information,
         patient,
         _) = read_test_data(test_file_name)
        _, student_count, student_hashes = self.run_disease_checker(
            table_size,
            disease_information,
            patient
        )
        self.assertEqual(student_count, StatCounter.get('comparisons'))
        self.assertEqual(student_hashes, StatCounter.get('hashes'))

    def comparisons_test(self, test_file_name, scale, target=None):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds, or target)
        """
        (table_size,
         disease_information,
         patient,
         true_answer) = read_test_data(test_file_name)
        if target is None:
            lower_bound, upper_bound = self.get_bounds(table_size,
                                                       len(disease_information),
                                                       len(patient),
                                                       len(true_answer),
                                                       scale)
        _, student_count, student_hashes = self.run_disease_checker(
            table_size,
            disease_information,
            patient
        )
        if target is not None:
            self.assertEqual(student_count, target)
        else:
            valid_count_range = range(lower_bound, upper_bound + 1)
            self.assertIn(student_count, valid_count_range)
        self.assertEqual(student_hashes,
                         len(patient) + len(disease_information))

    #== Tests with an empty dataset ==#

    def test_empty(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=0, present=0)
        self.common_genes_test(test_file)

    def test_empty_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=0, present=0)
        self.internal_comparisons_test(test_file)

    def test_empty_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=0, present=0)
        self.comparisons_test(test_file, 0)

    #== Tests with a trivially tiny dataset ==#

    def test_tiny(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=1, present=1)
        self.common_genes_test(test_file)

    def test_tiny_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=1, present=1)
        self.internal_comparisons_test(test_file)

    def test_tiny_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=1, db=1, present=1)
        self.comparisons_test(test_file, 1)

    #== Tests with a small dataset ==#

    def test_small_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(table=50, db=10, present=2)
        self.common_genes_test(test_file)

    def test_small_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=50, db=10, present=2)
        self.internal_comparisons_test(test_file)

    def test_small_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=50, db=10, present=2)
        self.comparisons_test(test_file, 0.5)

    def test_small_low_load(self):
        test_file = TEST_FILE_FORMAT.format(table=30, db=10, present=2)
        self.common_genes_test(test_file)

    def test_small_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=30, db=10, present=2)
        self.internal_comparisons_test(test_file)

    def test_small_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=30, db=10, present=2)
        self.comparisons_test(test_file, 0.3)

    def test_small_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(table=15, db=10, present=2)
        self.common_genes_test(test_file)

    def test_small_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=15, db=10, present=2)
        self.internal_comparisons_test(test_file)

    def test_small_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=15, db=10, present=2)
        self.comparisons_test(test_file, 0.3)

    def test_small_high_load(self):
        test_file = TEST_FILE_FORMAT.format(table=11, db=10, present=2)
        self.common_genes_test(test_file)

    def test_small_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=11, db=10, present=2)
        self.internal_comparisons_test(test_file)

    def test_small_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=11, db=10, present=2)
        self.comparisons_test(test_file, 0.55)

    def test_small_full_load(self):
        test_file = TEST_FILE_FORMAT.format(table=10, db=10, present=2)
        self.common_genes_test(test_file)

    def test_small_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=10, db=10, present=2)
        self.internal_comparisons_test(test_file)

    def test_small_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=10, db=10, present=2)
        self.comparisons_test(test_file, 1)

    #== Tests with a medium dataset ==#

    def test_medium_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=80, present=20)
        self.common_genes_test(test_file)

    def test_medium_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=80, present=20)
        self.internal_comparisons_test(test_file)

    def test_medium_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=80, present=20)
        self.comparisons_test(test_file, 0.1)

    def test_medium_low_load(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=80, present=20)
        self.common_genes_test(test_file)

    def test_medium_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=80, present=20)
        self.internal_comparisons_test(test_file)

    def test_medium_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=80, present=20)
        self.comparisons_test(test_file, 0.05)

    def test_medium_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(table=130, db=80, present=20)
        self.common_genes_test(test_file)

    def test_medium_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=130, db=80, present=20)
        self.internal_comparisons_test(test_file)

    def test_medium_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=130, db=80, present=20)
        self.comparisons_test(test_file, 0.1)

    def test_medium_high_load(self):
        test_file = TEST_FILE_FORMAT.format(table=90, db=80, present=20)
        self.common_genes_test(test_file)

    def test_medium_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=90, db=80, present=20)
        self.internal_comparisons_test(test_file)

    def test_medium_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=90, db=80, present=20)
        self.comparisons_test(test_file, 0.25)

    def test_medium_full_load(self):
        test_file = TEST_FILE_FORMAT.format(table=80, db=80, present=20)
        self.common_genes_test(test_file)

    def test_medium_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=80, db=80, present=20)
        self.internal_comparisons_test(test_file)

    def test_medium_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=80, db=80, present=20)
        self.comparisons_test(test_file, 1)

    #== Tests with a large dataset ==#

    def test_large_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(table=900, db=176, present=50)
        self.common_genes_test(test_file)

    def test_large_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=900, db=176, present=50)
        self.internal_comparisons_test(test_file)

    def test_large_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=900, db=176, present=50)
        self.comparisons_test(test_file, 0.1)

    def test_large_low_load(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=176, present=50)
        self.common_genes_test(test_file)

    def test_large_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=176, present=50)
        self.internal_comparisons_test(test_file)

    def test_large_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=400, db=176, present=50)
        self.comparisons_test(test_file, 0.1)

    def test_large_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(table=300, db=176, present=50)
        self.common_genes_test(test_file)

    def test_large_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=300, db=176, present=50)
        self.internal_comparisons_test(test_file)

    def test_large_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=300, db=176, present=50)
        self.comparisons_test(test_file, 0.1)

    def test_large_high_load(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=176, present=50)
        self.common_genes_test(test_file)

    def test_large_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=176, present=50)
        self.internal_comparisons_test(test_file)

    def test_large_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=200, db=176, present=50)
        self.comparisons_test(test_file, 0.1)

    def test_large_full_load(self):
        test_file = TEST_FILE_FORMAT.format(table=176, db=176, present=50)
        self.common_genes_test(test_file)

    def test_large_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=176, db=176, present=50)
        self.internal_comparisons_test(test_file)

    def test_large_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(table=176, db=176, present=50)
        self.comparisons_test(test_file, 1)


class TestGeneLookupChaining(BaseTestGeneLookup):
    """ Unit tests for the chaining hash table.
    """

    def run_disease_checker(self, table_size, disease_information, patient):
        return super().run_disease_checker(
            table_size, disease_information, patient,
            ChainingGeneHashTable
        )


class TestGeneLookupLinearProbing(BaseTestGeneLookup):
    """ Unit tests for the linear probing hash table.
    """

    def run_disease_checker(self, table_size, disease_information, patient):
        return super().run_disease_checker(
            table_size, disease_information, patient,
            LinearProbingGeneHashTable
        )

    def test_overfull_table(self):
        test_file = TEST_FILE_FORMAT.format(table=9, db=10, present=2)
        with self.assertRaises(IndexError):
            self.common_genes_test(test_file)


def all_tests_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGeneLookupChaining))
    # uncomment the next line when ready for linear probing
    suite.addTest(unittest.makeSuite(TestGeneLookupLinearProbing))
    return suite


def main():
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(all_tests_suite())

if __name__ == '__main__':
    main()


