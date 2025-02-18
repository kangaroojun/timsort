import time
import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from timsort import tim_sort

def benchmark_sorting(n=10000, min_run=32, num_tests=5):
    """Compares Python's built-in TimSort with custom TimSort.
    
    Parameters:
    n -- Size of the array to be sorted
    min_run -- Minimum run length for custom TimSort
    num_tests -- Number of times to run the benchmark

    Returns:
    None (prints results)
    """
    python_times = []
    custom_times = []
    
    for _ in range(num_tests):
        # Generate a random dataset
        test_array = [random.randint(-1000, 1000) for _ in range(n)]
        
        # Python's built-in TimSort
        py_array = test_array[:]
        start_time = time.perf_counter()
        py_sorted = sorted(py_array)  # Python's built-in sort
        end_time = time.perf_counter()
        python_times.append(end_time - start_time)

        # Custom TimSort
        custom_array = test_array[:]
        start_time = time.perf_counter()
        custom_sorted = tim_sort(custom_array, min_run)  # Your implementation
        end_time = time.perf_counter()
        custom_times.append(end_time - start_time)

        # Verify correctness
        assert custom_sorted == py_sorted, "Sorting results do not match!"

    # Print benchmarking results
    print(f"\nBenchmarking with array size: {n}, MinRun: {min_run}, Tests: {num_tests}")
    print(f"Python’s TimSort (sorted()): Avg time = {sum(python_times) / num_tests:.6f} sec")
    print(f"Custom TimSort: Avg time = {sum(custom_times) / num_tests:.6f} sec")

    if sum(custom_times) / num_tests > sum(python_times) / num_tests:
        print("\nYour TimSort is slower than Python's built-in sort.")
    else:
        print("\nYour TimSort is performing well!")

if __name__ == "__main__":
    benchmark_sorting(n=10000, min_run=32, num_tests=5)
