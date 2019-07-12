import glob
import unittest
from .convexhull import grahamscan
from .convexhull import readDataPts

test_files = glob.glob('A_*.dat')



class TestOne(unittest.TestCase):
    """Graham Scan"""
    def test_A_Files(self):
        for filename in test_files:
            print(filename)
            file = readDataPts(filename)
            print(grahamscan(file))


    def test_B_Files(self):
        self.assertEqual('a', 'a')


if __name__ == '__main__':
    unittest.main()

def __main__():
    unittest.main()