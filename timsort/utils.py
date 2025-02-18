def insertion_sort(arr, left, right):
    """Sorts a subarray using Insertion Sort.
    
    Input:
    arr -- list of integers
    left -- start index of the subarray
    right -- end index of the subarray
    
    Output:
    None (arr is modified in place)"""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def gallop_right(key, arr, start, end):
    """Returns the first index in arr[start:end] where arr[index] > key.
    This is used when the left run wins, to copy all elements that are <= key.

    Input:
    key -- element used for comparison
    arr -- modified array based on find_runs and previous merges
    start -- start index of the subarray
    end -- end index of the subarray

    Output:
    lo -- index of the first element > key"""
    lo = start
    hi = start + 1
    gallop_step = 1

    # Exponential search: move hi forward while elements are <= key.
    while hi < end and arr[hi] <= key:
        lo = hi
        hi = start + (gallop_step * 2)
        gallop_step *= 2

    hi = min(hi, end)
    # Binary search between lo and hi for the first element > key.
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= key: # Since copying from left run, we accept elements <= key to ensure stability
            lo = mid + 1
        else:
            hi = mid
    return lo

def gallop_left(key, arr, start, end):
    """Returns the first index in arr[start:end] where arr[index] >= key.
    This is used when the right run wins, to copy all elements that are < key.

    Input:
    key -- element used for comparison
    arr -- modified array based on find_runs and previous merges
    start -- start index of the subarray
    end -- end index of the subarray

    Output:
    lo -- index of the first element >= key"""
    lo = start
    hi = start + 1
    gallop_step = 1

    # Exponential search: move hi forward while elements are < key.
    while hi < end and arr[hi] < key:
        lo = hi
        hi = start + (gallop_step * 2)
        gallop_step *= 2

    hi = min(hi, end)
    # Binary search between lo and hi for the first element >= key.
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < key: # Since copying from right run, we do not accept elements = key to ensure stability
            lo = mid + 1
        else:
            hi = mid
    return lo

def find_runs(arr, min_run):
    """Detects natural runs in the array and extends short ones to at least min_run.
    
    Input:
    arr -- list of integers to be sorted
    min_run -- minimum run length
    
    Output:
    runs_stack -- list of tuples, each tuple contains the start and end index of a run
    arr -- modified array with runs extended to at least min_run"""
    runs_stack = []
    n = len(arr)
    i = 0

    while i < n:
        start = i
        # Detect ascending or descending sequence
        if i < n - 1 and arr[i] <= arr[i + 1]:  # Ascending
            while i < n - 1 and arr[i] <= arr[i + 1]:
                i += 1
        else:  # Descending
            while i < n - 1 and arr[i] > arr[i + 1]:
                i += 1
            arr[start:i+1] = arr[start:i+1][::-1]  # Reverse descending run to ascending

        run_length = i - start + 1
        if run_length < min_run:  # Extend run to min_run using Insertion Sort
            end = min(start + min_run - 1, n - 1)
            insertion_sort(arr, start, end)
            i = end

        runs_stack.append((start, i))  # Store the run boundaries
        i += 1

    return runs_stack, arr