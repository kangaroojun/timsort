from .utils import find_runs, gallop_right, gallop_left

def gallop_mode(arr, left_part, right_part, i, j, k):
    """Switches to galloping mode when one run wins too many times.

    Input:
    arr -- modified array based on find_runs
    left_part -- left run to be merged
    right_part -- right run to be merged
    i -- index of left_part
    j -- index of right_part
    k -- current index of pointer in arr

    Output:
    i -- updated index of left_part
    j -- updated index of right_part
    k -- updated index of pointer in arr"""
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            # Left run wins: copy a block from left_part.
            # Find the first index in left_part where the element is > right_part[j].
            gallop_index = gallop_right(right_part[j], left_part, i, len(left_part))
            while i < gallop_index:
                arr[k] = left_part[i]
                i += 1
                k += 1
            return i, j, k
        else:
            # Right run wins: copy a block from right_part.
            # Find the first index in right_part where the element is >= left_part[i].
            gallop_index = gallop_left(left_part[i], right_part, j, len(right_part))
            while j < gallop_index:
                arr[k] = right_part[j]
                j += 1
                k += 1
            return i, j, k

    return i, j, k

def merge(arr, left, mid, right, min_gallop):
    """Merge two sorted subarrays using galloping mode when appropriate.
    
    Input:
    arr -- modified array based on find_runs
    left -- start index of the first run to be merged
    mid -- end index of the first run to be merged
    right -- end index of the second run to be merged
    min_gallop -- minimum galloping mode threshold
    
    Output:
    None (arr is modified in place)"""
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i = j = 0
    k = left
    left_wins = 0  # Tracks consecutive wins for left
    right_wins = 0  # Tracks consecutive wins for right

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
            left_wins += 1
            right_wins = 0
        else:
            arr[k] = right_part[j]
            j += 1
            right_wins += 1
            left_wins = 0
        k += 1

        # If one side wins too many times, switch to galloping mode.
        if left_wins >= min_gallop and i < len(left_part):
            left_wins = 0  # Reset win counter
            i, j, k = gallop_mode(arr, left_part, right_part, i, j, k)
        elif right_wins >= min_gallop and j < len(right_part):
            right_wins = 0  # Reset win counter
            i, j, k = gallop_mode(arr, left_part, right_part, i, j, k)
    
    # Copy any remaining elements
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1

def merge_at(arr, run_stack, i, min_gallop):
    """Merges the run at index i with the next run in the stack.
    
    Input:
    arr -- modified array based on find_runs
    run_stack -- list of tuples containing the start and end index of runs
    i -- index of the first run to be merged, obtained from running merge_collapse
    min_gallop -- minimum galloping mode threshold
    
    Output:
    None (arr and run_stack are modified in place)"""
    left, mid = run_stack[i]
    right = run_stack[i + 1][1]

    merge(arr, left, mid, right, min_gallop)

    # Update the run stack after merging
    run_stack[i] = (left, right)
    del run_stack[i + 1]

def merge_collapse(arr, run_stack, min_gallop):
    """Enforces TimSort's merging conditions to keep merges balanced.
    
    Input:
    arr -- modified array based on find_runs
    run_stack -- list of tuples containing the start and end index of runs, obtained from find_runs
    min_gallop -- minimum galloping mode threshold
    
    Output:
    None (arr and run_stack are modified in place)"""
    merged = False
    while len(run_stack) > 1:
        n = len(run_stack) - 1

        if n > 1 and run_stack[n - 2][1] - run_stack[n - 2][0] <= \
                    run_stack[n - 1][1] - run_stack[n - 1][0] + \
                    run_stack[n][1] - run_stack[n][0]:
            if run_stack[n - 2][1] - run_stack[n - 2][0] < run_stack[n][1] - run_stack[n][0]:
                merge_at(arr, run_stack, n - 2, min_gallop)
            else:
                merge_at(arr, run_stack, n - 1, min_gallop)
            merged = True
        elif run_stack[n - 1][1] - run_stack[n - 1][0] <= run_stack[n][1] - run_stack[n][0]:
            merge_at(arr, run_stack, n - 1, min_gallop)
            merged = True
        else:
            break  # No merge triggered by the invariants

    # If no merges were performed, force merge the last two runs.
    if not merged and len(run_stack) > 1:
        merge_at(arr, run_stack, len(run_stack) - 2, min_gallop)

def tim_sort(arr, min_run=32, min_gallop=7):
    """Performs TimSort algorithm on the given array.
    
    Input:
    arr -- list of integers to be sorted
    min_run -- minimum run length
    
    Output:
    arr -- sorted array"""
    runs, arr = find_runs(arr, min_run)
    run_stack = runs[:]  # Copy the runs to be managed as a stack

    while len(run_stack) > 1:
        merge_collapse(arr, run_stack, min_gallop)

    return arr