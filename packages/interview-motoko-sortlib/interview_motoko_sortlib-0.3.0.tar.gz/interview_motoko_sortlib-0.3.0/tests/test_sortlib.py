import numpy as np
from sortlib import sort


def test_sort():
    arr = np.array([5.0, 3.0, 1.0, 4.0])
    sorted_arr = sort(arr.copy())
    assert np.array_equal(sorted_arr, np.array([1.0, 3.0, 4.0, 5.0]))
