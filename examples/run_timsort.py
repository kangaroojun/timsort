import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from timsort import tim_sort

test_array = [random.randint(-1000, 1000) for _ in range(10000)]

sorted_array = tim_sort(test_array[:], min_run=32, min_gallop=7)

print("Sorted array: ", sorted_array)