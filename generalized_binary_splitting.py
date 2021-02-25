import math
from bisect import bisect_left
from typing import Any, Callable, List, Tuple


def generalized_binary_splitting(
    pred: Callable[[List[Any],], bool],
    candidates: List[Any],
    d: int
) -> List[Any]:
    """Generalized binary-splitting algorithm for group testing
    https://en.wikipedia.org/wiki/Group_testing#Generalised_binary-splitting_algorithm

    Arguments
    ---------
    pred : callable
        Test function. Takes a list of items, and returns True if
        _any_ of the items are defective, and False otherwise.
    candidates : list
        Candidate pool
    d : int
        Upper bound on the number of defective items in the pool.

    Returns
    -------
    defective : List
        list of defective items
    """
    n = len(candidates)
    if n == 1 or n <= 2*d - 2:
        # test items individually
        return [c for c in candidates if pred([c])]
    else:
        l = n - d + 1
        alpha = math.floor(math.log2(l / 2))
        test_set = candidates[:2**alpha]
        remaining_set = candidates[2**alpha:]
        if pred(test_set):
            defect, nondefective = _binary_search(pred, test_set)
            remaining = list(set(candidates) - {defect} - set(nondefective))
            return [defect] + generalized_binary_splitting(pred, remaining, d-1)
        else:
            return generalized_binary_splitting(pred, remaining_set, d)


def _binary_search(
    pred: Callable[[List[Any],], bool],
    candidates: List[Any]
) -> Tuple[Any, List[Any]]:

    mid = 0
    start = 0
    end = len(candidates)
    nondefective = []

    while (start < end - 1):
        mid = (start + end) // 2

        test_set = candidates[start:mid]
        if pred(test_set):
            end = mid
        else:
            nondefective.extend(test_set)
            start = mid

    return candidates[start], nondefective


def test_binary_search():
    candidates = list(range(100))
    for c in candidates:
        res, non_defective = _binary_search((lambda x: c in x), candidates)
        assert res == c


def test_generalized_binary_splitting():
    def pred(xs):
        # print("testing", xs)
        return (0 in xs) or (32 in xs)

    candidates = list(range(100))
    import random
    random.shuffle(candidates)

    assert sorted(generalized_binary_splitting(pred, candidates, d=2)) == [0, 32]


if __name__ == "__main__":
    test_binary_search()
    for i in range(100):
        test_generalized_binary_splitting()
