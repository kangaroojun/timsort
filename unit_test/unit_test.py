import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from timsort import tim_sort

class TestTimSort(unittest.TestCase):
    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(tim_sort(arr, min_run=4), sorted(arr))

    def test_reverse_array(self):
        arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(tim_sort(arr, min_run=4), sorted(arr))

if __name__ == '__main__':
    unittest.main()