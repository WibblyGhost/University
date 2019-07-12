"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""

import unittest
import math

from classes import Gene, Genome, GeneList
from utilities import StatCounter, read_test_data

from genetic_similarity_sequential import genetic_similarity_sequential
from genetic_similarity_binary import genetic_similarity_binary


TEST_FILE_FORMAT = "TestData/test_data-{size}-{common}.txt"


class TypeAssertion(object):

    def assertTypes(self, a, b):
        if type(a) != type(b):
            raise AssertionError("Type {} does not match type {}".format(
                type(a), type(b)
            ))


class BaseTestCommonGenes(unittest.TestCase, TypeAssertion):

    def setUp(self):
        """Runs before every test case"""
        for counter in {'comparisons', 'accesses', 'hashes', 'memory'}:
            StatCounter.reset(counter)

    def get_bounds(self, left_length, right_length):
        raise NotImplementedError("This method should be "
                                  "implemented by a subclass.")

    def common_genes_test(self, test_file_name,
                          genetic_similarity_function):
        """ Test that the given genetic_similarity_function returns the correct
            result for the file specified by test_file_name.
        """
        (first_genome,
         second_genome,
         true_answer) = read_test_data(test_file_name)
        student_answer, _ = genetic_similarity_function(first_genome,
                                                        second_genome)
        self.assertEqual(student_answer, true_answer)
        self.assertTypes(student_answer, true_answer)

    def internal_comparisons_test(self, test_file_name,
                                  genetic_similarity_function):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
        """
        (first_genome,
         second_genome, _) = read_test_data(test_file_name)
        _, student_count = genetic_similarity_function(first_genome,
                                                       second_genome)
        self.assertEqual(student_count, StatCounter.get('comparisons'))

    def comparisons_test(self, test_file_name, genetic_similarity_function,
                         target=None):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds, or target)
        """
        (first_genome,
         second_genome, _) = read_test_data(test_file_name)
        if target is None:
            lower_bound, upper_bound = self.get_bounds(len(first_genome),
                                                       len(second_genome))
        _, student_count = genetic_similarity_function(first_genome,
                                                       second_genome)
        if target is not None:
            self.assertEqual(student_count, target)
        else:
            valid_count_range = range(lower_bound, upper_bound + 1)
            try:
                self.assertIn(student_count, valid_count_range)
            except AssertionError:
                raise AssertionError("{} is not in range {}-{}".format(
                    student_count, lower_bound, upper_bound
                ))

    #== Tests with an empty dataset ==#

    def test_empty(self):
        test_file = TEST_FILE_FORMAT.format(size=0, common=0)
        self.common_genes_test(test_file)

    def test_empty_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=0, common=0)
        self.internal_comparisons_test(test_file)

    def test_empty_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=0, common=0)
        self.comparisons_test(test_file, 0)

    #== Tests with a trivially tiny dataset ==#

    def test_tiny(self):
        test_file = TEST_FILE_FORMAT.format(size=2, common=1)
        self.common_genes_test(test_file)

    def test_tiny_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=2, common=1)
        self.internal_comparisons_test(test_file)

    def test_tiny_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=2, common=1)
        self.comparisons_test(test_file)

    #== Tests with a small dataset ==#

    def test_small_none_common(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=0)
        self.common_genes_test(test_file)

    def test_small_none_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=0)
        self.internal_comparisons_test(test_file)

    def test_small_none_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=0)
        self.comparisons_test(test_file)

    def test_small_some_common(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=3)
        self.common_genes_test(test_file)

    def test_small_some_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=3)
        self.internal_comparisons_test(test_file)

    def test_small_some_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=3)
        self.comparisons_test(test_file)

    def test_small_all_common(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=10)
        self.common_genes_test(test_file)

    def test_small_all_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=10)
        self.internal_comparisons_test(test_file)

    def test_small_all_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=10)
        self.comparisons_test(test_file)

    #== Tests with a large dataset ==#

    def test_large_none_common(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=0)
        self.common_genes_test(test_file)

    def test_large_none_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=0)
        self.internal_comparisons_test(test_file)

    def test_large_none_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=0)
        self.comparisons_test(test_file)

    def test_large_some_common(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=250)
        self.common_genes_test(test_file)

    def test_large_some_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=250)
        self.internal_comparisons_test(test_file)

    def test_large_some_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=250)
        self.comparisons_test(test_file)

    def test_large_all_common(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=1000)
        self.common_genes_test(test_file)

    def test_large_all_common_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=1000)
        self.internal_comparisons_test(test_file)

    def test_large_all_common_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=1000)
        self.comparisons_test(test_file)


class TestCommonGenesSequential(BaseTestCommonGenes):
    """ Unit tests for the sequential common gene finder.
    """

    def get_bounds(self, m, n):
        return m, m * n

    def common_genes_test(self, test_file_name):
        super().common_genes_test(test_file_name,
                                  genetic_similarity_sequential)

    def internal_comparisons_test(self, test_file_name):
        super().internal_comparisons_test(test_file_name,
                                          genetic_similarity_sequential)

    def comparisons_test(self, test_file_name, expected=None):
        super().comparisons_test(test_file_name,
                                 genetic_similarity_sequential,
                                 expected)

    # Here we do some extra tests with known values

    def test_tiny_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=2, common=1)
        self.comparisons_test(test_file, 4)

    def test_small_none_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=0)
        self.comparisons_test(test_file, 100)

    def test_small_some_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=3)
        self.comparisons_test(test_file, 85)

    def test_small_all_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=10, common=10)
        self.comparisons_test(test_file, 55)

    def test_large_none_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=0)
        self.comparisons_test(test_file, 1000000)

    def test_large_some_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=250)
        self.comparisons_test(test_file, 869402)

    def test_large_all_common_comparisons_exact(self):
        test_file = TEST_FILE_FORMAT.format(size=1000, common=1000)
        self.comparisons_test(test_file, 500500)


class TestCommonGenesBinary(BaseTestCommonGenes):
    """ Unit tests for the binary search common gene finder.
    """

    def get_bounds(self, m, n):
        logn = int(math.log(n, 2))
        lower = m * (logn + 1) - 2
        upper = m * (logn + 2) + 2
        return lower, upper

    def common_genes_test(self, test_file_name):
        super().common_genes_test(test_file_name, genetic_similarity_binary)

    def internal_comparisons_test(self, test_file_name):
        super().internal_comparisons_test(test_file_name,
                                          genetic_similarity_binary)

    def comparisons_test(self, test_file_name, expected=None):
        super().comparisons_test(test_file_name,
                                 genetic_similarity_binary,
                                 expected)


def all_tests_suite():
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestCommonGenesSequential))
    # uncomment the next line when ready for binary testing
    suite.addTest(unittest.makeSuite(TestCommonGenesBinary))
    return suite


def main():
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(all_tests_suite())

if __name__ == '__main__':
    main()
